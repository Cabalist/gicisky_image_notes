from typing import Iterator, List, Union

from formatting import get_chunks

# FIXME Data is reversed on the byte level when recreating lines
# FIXME Data is reversed as a whole line as well
# FIXME There is still a zero padding issue see the line: 000000ff2203800000f0ffff1f0000c0ffff7f000000ffffff010000fcffff070084000000402875

# TODO:  I now have can successfully move an 8px line across the screen.  I need to make my recreate line function separate and write tests.



PATH_TO_FILE = "unformatted_8px_lines.txt"
# PATH_TO_FILE = "successful_img_captures/25px_checkerboard_black_white/big_endian_formatted_image_data.hex"

compression_marker_lookup_table = {
    "000f": "110000",
    "000e": "100000",
    "000d": "0F0000",
    "000c": "0E0000",
    "000b": "0D0000",
    "000a": "0C0000",
    "0009": "0B0000",
    "0008": "0A0000",
    "0007": "090000",
    "0006": "080000",
    "0005": "070000",
    "0004": "060000",
    "0003": "050000",
    "0002": "040000",
    "0001": "030000",
}


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def swap_endianness(image_line: str) -> str:
    return "".join(reversed(get_chunks(image_line, 2)))


def replace_all_chrs(a_list: List[str], a_chr: str) -> Iterator[str]:
    for each_word in a_list:
        yield a_chr * len(each_word)


# def get_suffix_annotation(bit_pattern: str, data_bytes_in_line: str, line_length_in_bytes: str, end_of_line: str) -> List[str]:
#     suffix = [bit_pattern, data_bytes_in_line, line_length_in_bytes, end_of_line]
#     lines = []
#     lines.append(" ".join(suffix))
#     lines.append(" ".join(replace_all_chrs(suffix, "⬆")))
#     lines.append(" ".join(replace_all_chrs(suffix, "|")))
#     lines.append(" ".join(replace_all_chrs(suffix[:-1], "|")) + "  End of line")
#     lines.append(" ".join(replace_all_chrs(suffix[:-2], "|")) + f"  Line Length in Bytes ({int(line_length_in_bytes, 16)}B)")
#     lines.append(" ".join(replace_all_chrs(suffix[:-3], "|")) + f"  Line represents this many bytes ({int(data_bytes_in_line, 16)}B) ({int(data_bytes_in_line, 16) * 8}b)")
#     lines.append("Bit pattern for compression markers")
#     lines.append("    └" + " ".join(get_chunks(f"{int(bit_pattern, 16):b}", 4)))
#
#     return lines


def get_polarity_of_compression_markers(arrow_chunks: List[str]) -> List[Union[None, str]]:
    simplified_order = [arrow[0] for arrow in arrow_chunks]

    polarity_list = []
    last_one = True
    for i, each in enumerate(reversed(simplified_order)):
        if each == "⬆" and last_one:
            last_one = False
            if list(reversed(simplified_order))[i + 1] == "⬆":
                polarity = "Left"
            else:
                polarity = "Right"
        elif each == "⬆":
            polarity = "Left"
        else:
            polarity = None
        polarity_list.append(polarity)
    return list(reversed(polarity_list))


def get_labels_for_data_line(formatted_data_line: str, arrow_line: str) -> List[str]:
    labels = []
    data_chunks = formatted_data_line.split(" ")
    arrow_chunks = arrow_line.split(" ")

    polarity_list = get_polarity_of_compression_markers(arrow_chunks)

    for i, each_chunk in enumerate(data_chunks):

        # The compression mark logic would seem to work like this:
        # The last one must pull from the RIGHT.
        #    UNLESS it next to another one then it pulls from the LEFT.
        # All other compression markers pull from the LEFT

        if "⬆" in arrow_chunks[i]:
            # This is a compression marker

            if len(each_chunk) == 4:
                compression_marker = compression_marker_lookup_table.get(each_chunk, None)
            else:
                compression_marker = each_chunk
            if compression_marker is not None:
                polarity = polarity_list[i]

                labels.append(f"There are {int(compression_marker[:2], 16)} bytes (0x{compression_marker[:2]}) of the {polarity} single byte pattern {'<-' if polarity == 'Left' else '->'}")
            else:
                labels.append(f"{Bcolors.FAIL}Unknown compression marker: {each_chunk}{Bcolors.ENDC}")
        elif "⇧" in arrow_chunks[i]:
            # This is data
            bit_string_label = ""

            # Our hex conversion is throwing away the leading zeros on multibyte chunks.  I'll manually save them here.
            if len(each_chunk) > 2:
                for each_byte in get_chunks(each_chunk, 2):
                    if each_byte == "00":
                        bit_string_label += "00000000 "
                    else:
                        break

            # FIXME This should point me to my endian swap being wrong
            # HACK!!! This was coming out with all bytes in reverse but not the orders of the bytes.  I think this is a side effect of my endian swap. But I'm just reversing them here.
            bit_string_label += " ".join(c[::-1] for c in get_chunks(f"{int(each_chunk, 16):08b}", 8))
            labels.append(bit_string_label)
        else:
            raise ValueError("Found bit value without label.")

    return list(reversed(labels))


def recreate_line(formatted_data_line: str, arrow_line: str) -> str:
    data_chunks = formatted_data_line.split(" ")
    arrow_chunks = arrow_line.split(" ")

    polarity_list = get_polarity_of_compression_markers(arrow_chunks)

    uncompressed_line = ""
    last_byte = ""
    byte_multiplier = 1
    for i, each_chunk in enumerate(data_chunks):
        if not each_chunk:
            continue
        if "⬆" in arrow_chunks[i]:
            # This is a compression marker
            if len(each_chunk) == 4:
                compression_marker = compression_marker_lookup_table.get(each_chunk, None)
            else:
                compression_marker = each_chunk

            if compression_marker is not None:
                if polarity_list[i] == "Left":
                    print(f"Compression Marker: {Bcolors.BOLD}{each_chunk}{Bcolors.ENDC} expanded this byte: {Bcolors.BOLD}{last_byte}{Bcolors.ENDC}")
                    uncompressed_line += int(compression_marker[:2], 16) * f"{int(last_byte, 16):08b}"
                if polarity_list[i] == "Right":
                    byte_multiplier = int(compression_marker[:2], 16)
                    print(f"Compression Marker: {Bcolors.BOLD}{each_chunk}{Bcolors.ENDC} expanded this byte: {Bcolors.BOLD}{data_chunks[i + 1][:2]}{Bcolors.ENDC}")

            else:
                print(f"{Bcolors.FAIL}WARNING: {Bcolors.WARNING}Unknown compression marker: {each_chunk}{Bcolors.ENDC}")
                uncompressed_line += "XXX"

        elif "⇧" in arrow_chunks[i]:
            # This is data
            for each_byte in get_chunks(each_chunk, 2):
                if byte_multiplier > 1:
                    uncompressed_line += f"{int(each_byte, 16):08b}" * byte_multiplier
                    byte_multiplier = 1

                uncompressed_line += f"{int(each_byte, 16):08b}"

                last_byte = each_byte
        else:
            raise ValueError(f"Found bit value without label: {arrow_chunks[i]}")


    if len(uncompressed_line) != 512:
        len_diff = 512 - len(uncompressed_line)
        print(f"{Bcolors.FAIL}WARNING: {Bcolors.WARNING}Line length is too {'short' if len_diff > 0 else 'long'}.  Expected: 512   Actual: {len(uncompressed_line)}  Difference: {Bcolors.FAIL if len_diff > 0 else Bcolors.OKGREEN}{512 - len(uncompressed_line)}{Bcolors.ENDC}")

    print(uncompressed_line.replace("0", "█").replace("1", " "))
    print("".join(get_chunks(uncompressed_line, 8)))
    print(("┕" + "━" * 6 + "┙") * 64)

    for i in range(64):
        i = f"{i:02}"
        print(f"{i:^8}", end="")
    print()

    bin_chunks = get_chunks(uncompressed_line, 8)
    for i in range(64):
        this_chunk = bin_chunks[int(i)]
        hex_rep = f"(0x{int(this_chunk[:4], 2):X}{int(this_chunk[4:], 2):X})"
        print(f"{hex_rep:^8}", end="")
    print()

    return uncompressed_line


def parse_lines() -> None:
    with open(PATH_TO_FILE) as raw_lines:
        for i, line in enumerate(raw_lines):
            line = line.strip()
            if line.startswith("#"):
                continue
            print(f"Line: {i}")

            # line = swap_endianness(line)
            print(line)

            remaining_line = line
            end_of_line = remaining_line[-2:]
            remaining_line = remaining_line[:-2]
            line_length_in_bytes = remaining_line[-2:]
            remaining_line = remaining_line[:-2]
            data_bytes_in_line = remaining_line[-2:]
            remaining_line = remaining_line[:-2]
            bit_pattern = remaining_line[-8:]
            remaining_line = remaining_line[:-8]

            bin_bit_pattern = f"{int(bit_pattern, 16):b}"

            formatted_remaining_line = ""
            arrow_line = ""

            for each_char in reversed(bin_bit_pattern):
                if not remaining_line:
                    continue
                if each_char == "0":
                    formatted_remaining_line = remaining_line[-2:] + formatted_remaining_line
                    arrow_line = "⇧⇧" + arrow_line
                    remaining_line = remaining_line[:-2]
                if each_char == "1":
                    compression_marker = remaining_line[-4:]
                    if compression_marker == "0000":
                        compression_marker = remaining_line[-6:]
                        remaining_line = remaining_line[:-6]
                        arrow_line = " ⬆⬆⬆⬆⬆⬆ " + arrow_line
                    else:
                        remaining_line = remaining_line[:-4]
                        arrow_line = " ⬆⬆⬆⬆ " + arrow_line

                    formatted_remaining_line = " " + compression_marker + " " + formatted_remaining_line
            else:
                if remaining_line:
                    formatted_remaining_line = remaining_line + formatted_remaining_line
                    arrow_line = "⇧" * len(remaining_line) + arrow_line

            formatted_remaining_line = formatted_remaining_line.replace("  ", " ").strip()
            arrow_line = arrow_line.replace("  ", " ").strip()

            up_bar_line = ""
            for each_chr in arrow_line:
                if each_chr == " ":
                    up_bar_line += " "
                else:
                    up_bar_line += "|"

            data_labels = get_labels_for_data_line(formatted_remaining_line, arrow_line)

            suffix = get_suffix_annotation(bit_pattern, data_bytes_in_line, line_length_in_bytes, end_of_line)
            suffix[0] = formatted_remaining_line + " " + suffix[0]
            suffix[1] = arrow_line + " " + suffix[1]
            suffix[2] = up_bar_line + " " + suffix[2]
            suffix[3] = up_bar_line + " " + suffix[3]
            suffix[4] = up_bar_line + " " + suffix[4]
            suffix[5] = up_bar_line + " " + suffix[5]
            suffix[6] = up_bar_line + " " + suffix[6]
            suffix[7] = up_bar_line + " " + suffix[7]
            suffix.append(up_bar_line)
            for idx, each_label in enumerate(data_labels):
                suffix.append(" ".join(up_bar_line.split()[:-1 * (idx + 1)]) + "  " + data_labels[idx])

            print("\n".join(suffix))
            print("\n")
            recreate_line(formatted_remaining_line, arrow_line)
            print("\n")
            print("-" * 512)


parse_lines()
