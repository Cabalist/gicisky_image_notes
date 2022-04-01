from itertools import groupby, zip_longest
from typing import Iterator, List, Tuple

from decompress import decode_compression_marker, get_binary_of_compression_pattern, parse_suffix, recreate_line, split_label_line_data
from utils.common import Bcolors, get_chunks

VERTICAL_BAR = "┊"

INSTRUCTION_ARROW = "I"
DATA_ARROW = "D"

def replace_all_chrs(a_list: List[str], a_chr: str) -> Iterator[str]:
    for each_word in a_list:
        yield a_chr * len(each_word)


def get_suffix_annotation(bit_pattern: str, data_bytes_in_line: str, line_length_in_bytes: str, end_of_line: str, annotation_stack_height: int) -> List[str]:
    suffix = [end_of_line, line_length_in_bytes, data_bytes_in_line, bit_pattern]
    lines = []
    lines.append(" ".join(suffix) + " ")
    lines.append(" ".join(replace_all_chrs(suffix, INSTRUCTION_ARROW)) + " ")
    for i in range(annotation_stack_height - 1):
        lines.append(" ".join(replace_all_chrs(suffix, VERTICAL_BAR)) + " ")
    lines.append(" ".join(replace_all_chrs(suffix[:-1], VERTICAL_BAR)) + "  Bit pattern for compression markers")
    lines.append(" ".join(replace_all_chrs(suffix[:-1], VERTICAL_BAR)) + "    └ " + " ".join(get_chunks(get_binary_of_compression_pattern(bit_pattern), 4)))
    lines.append(" ".join(replace_all_chrs(suffix[:-1], VERTICAL_BAR)) + "    └     * Applied in reverse")
    lines.append(" ".join(replace_all_chrs(suffix[:-1], VERTICAL_BAR)))
    lines.append(" ".join(replace_all_chrs(suffix[:-2], VERTICAL_BAR)) + f"  Line represents this many bytes ({int(data_bytes_in_line, 16)}B) ({int(data_bytes_in_line, 16) * 8}b)")
    lines.append(" ".join(replace_all_chrs(suffix[:-3], VERTICAL_BAR)) + f"  Line Length in bytes ({int(line_length_in_bytes, 16)}B) (36 characters)")

    lines.append("End of Line")

    return lines


def annotate_data(data_chunk: str) -> str:
    line = ""
    for each_byte in get_chunks(data_chunk, 2):
        line += f" {int(each_byte, 16):08b}"
    return line


def annotate_compression_marker(labeled_line: List[Tuple[str, str]], compression_chunk_idx: int, first_marker: bool) -> str:
    compression_marker = labeled_line[compression_chunk_idx][1]

    if first_marker and labeled_line[compression_chunk_idx + 1][0] != "compression":
        polarity = "Left"
    else:
        polarity = "Right"

    if polarity == "Left":
        if labeled_line[compression_chunk_idx - 1][0] == "compression":
            offset = -2
        else:
            offset = -1
        byte_to_decompress = labeled_line[compression_chunk_idx + offset][1][-2:].upper()
    else:

        if labeled_line[compression_chunk_idx + 1][0] == "compression":
            offset = 2
        else:
            offset = 1
        byte_to_decompress = labeled_line[compression_chunk_idx + offset][1][:2].upper()
    try:
        multiplier = decode_compression_marker(compression_marker)
    except ValueError as e:
        print(f"{Bcolors.FAIL}Unknown compression marker: {compression_marker}{Bcolors.ENDC}")
        multiplier = 0

    return f" There are {multiplier} bytes (0x{multiplier:X}) of 0x{byte_to_decompress} ({'<-' if polarity == 'Left' else '->'} {polarity} single byte pattern {'<-' if polarity == 'Left' else '->'})"


def get_data_annotation(labeled_line):
    arrow_line = []
    value_line = []
    lines = []

    # First we create the arrows and the lines pointing to those arrows
    _just_values = [v[1] for v in labeled_line]
    lines.append(" ".join(replace_all_chrs(_just_values, VERTICAL_BAR)) + " ")
    for i, (label, value) in enumerate(labeled_line):
        if i:
            lines.append(" ".join(replace_all_chrs(_just_values[:-1 * i], VERTICAL_BAR)) + " ")
        value_line.append(value)
        if label == "data":
            arrow_line.append(DATA_ARROW * len(value))
        elif label == "compression":
            arrow_line.append(INSTRUCTION_ARROW * len(value))
        else:
            raise ValueError(f"Unknown data label: {label}")

    lines.append("")  # Final Label line

    # Now we create the actual labels
    first_marker = True
    for i, (label, value) in enumerate(labeled_line):
        if label == "data":
            lines[len(lines) - 1 - i] += annotate_data(value)

        elif label == "compression":
            lines[len(lines) - 1 - i] += annotate_compression_marker(labeled_line, i, first_marker)
            first_marker = False

        else:
            raise ValueError(f"Unknown data label: {label}")

    return [" ".join(value_line), " ".join(arrow_line), *lines]


def main():
    LINES_TO_EXAMINE = [
        "751a400010008000ff00ff00ff00ff00ffffff000030ffffffff",
        "751c400040008000ff00ff00ff00ff00ff00ffffff00002effffffff",
        "7520400000048000ff00ff00ff00ff00ff00ff00ff00ffffff00002affffffff",
        "7522400000108000ff00ff00ff00ff00ff00ff00ff00ff00ffffff000028ffffffff",
        "7524400000408000ff00ff00ff00ff00ff00ff00ff00ff00ff00ffffff000026ffffffff",
        "7526400000008100ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ffffff000024ffffffff",
        "7528400000008400ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ffffff000022ffffffff",
        "752e400000009000ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ffffff000020ffff00000080ffff",
        "753040000000c000ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ffffff00001e00000080ffffffff",
        "7532400000008000ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ffff02000080ff00001cffffffff",
        "7534400000008000ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff0008000080ffffff00001affffffff",
        "75374000000080007f007f007f007f007f007f007f007f007f007f007f007f007f007f007f00400000807f007fffffff000017ffffffff",
        "7538400000008000ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff00ff0080000080ff00ff00ffffff000016ffffffff",

        ]

    for each_line in LINES_TO_EXAMINE:
        print("═" * 512)

        suffix = parse_suffix(each_line)
        split_line = split_label_line_data(suffix["remaining_line"], get_binary_of_compression_pattern(suffix['bit_pattern']))
        data_annotations = get_data_annotation(split_line)
        suffix_annotations = get_suffix_annotation(bit_pattern=suffix['bit_pattern'], data_bytes_in_line=suffix['data_bytes_in_line'], line_length_in_bytes=suffix['line_length_in_bytes'], end_of_line=suffix['end_of_line'], annotation_stack_height=len(data_annotations))

        annotations = zip_longest(suffix_annotations, data_annotations, fillvalue="")

        for each in annotations:
            print("".join(each))

        print()
        uncompressed_line = recreate_line(each_line)

        if len(uncompressed_line) != 512:
            len_diff = 512 - len(uncompressed_line)
            print(f"{Bcolors.FAIL}WARNING: {Bcolors.WARNING}Line length is too {'short' if len_diff > 0 else 'long'}.  Expected: 512   Actual: {len(uncompressed_line)}  Difference: {Bcolors.FAIL if len_diff > 0 else Bcolors.OKGREEN}{512 - len(uncompressed_line)}{Bcolors.ENDC}")

        print()

        groups = groupby(uncompressed_line)
        result = [(label, sum(1 for _ in group)) for label, group in groups]
        run_line_labels = ""
        run_line_labels_hex = ""
        run_line = ""
        for _, count in result:
            if count == 1:
                run_line += "│"
                run_line_labels += "1"
                run_line_labels_hex += "1"
            else:
                run_line += "╭"
                for _ in range(count - 2):
                    run_line += "─"
                run_line += "╮"
                run_line_labels += f"{count:^{count}}"
                if count > 3:
                    count_as_padded_hex = f"0x{count:02X}"
                else:
                    count_as_padded_hex = str(count)
                run_line_labels_hex += f"{count_as_padded_hex:^{count}}"

        print(run_line_labels_hex)
        print(run_line_labels)
        print(run_line)

        print(uncompressed_line.replace("0", "█").replace("1", " "))
        print("".join(get_chunks(uncompressed_line, 8)))
        print(("┕" + "━" * 6 + "┙") * 64)

        for i in range(64):
            i = f"{i:02}"
            print(f"{i:^8}", end="")
        print()

        bin_chunks = get_chunks(uncompressed_line, 8)
        for each in bin_chunks:
            hex_rep = f"(0x{int(each[:4], 2):X}{int(each[4:], 2):X})"
            print(f"{hex_rep:^8}", end="")
        print()
        print()


main()
