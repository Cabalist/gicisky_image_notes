import os

from PIL import Image

CHUNK_SIZE = 36


def get_chunks(a_str, chunk_size):
    return [a_str[i:i + chunk_size] for i in range(0, len(a_str), chunk_size)]


def get_binary_chunks(a_str, chunk_size):
    for each_byte in get_chunks(a_str, chunk_size):
        # print(f"{int(each_byte, 16):08b}")
        yield f"{int(each_byte, 16):08b}"


def create_image_from_binary(data, width, height):
    print(f"Height: {height}")
    print(f"Width: {width}")

    im = Image.new('L', (width, height), "black")

    cmap = {'0': 0,
            '1': 255,
            'e': 100}

    data = [cmap[bit] for bit in data]

    im.putdata(data)
    return im


def create_ascii_image_from_binary(data, width, height):
    cmap = {'0': "░",
            '1': "█",
            'e': "X"}

    with open("ascii_image_format.txt", "w") as output:
        for each_chunk in get_chunks(data, width):
            for c in each_chunk:
                output.write(cmap[c])
            output.write("\n")

for each_file in os.listdir("successful_img_captures"):
    if not each_file.endswith(".txt"):
        continue
    output_dir = os.path.join("successful_img_captures", os.path.splitext(each_file)[0])
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join("successful_img_captures", each_file)) as f, \
            open(os.path.join(output_dir, "formatted_image_data.hex"), "w") as hex_output, \
            open(os.path.join(output_dir, "big_endian_formatted_image_data.hex"), "w") as big_endian_hex_output, \
            open(os.path.join(output_dir, "formatted_image_data.bin"), "w") as bin_output:

        image_data = ""
        first_line = True
        for each_line in f:
            # Line number is first 8 bytes (64bit)
            # 2a000000 -> 0000 002a (42)
            line_number = each_line[:8]
            # output.write(line_number + "\n")
            if first_line:
                # On the first line is the image size.  In this case:
                # 983a0000 -> 0000 3a98 (15000)
                image_size = each_line[8:16]
                print(image_size)
                # output.write(image_size + "\n")
                first_line = False
                remaining_line = each_line[16:]
            else:
                remaining_line = each_line[8:]

            image_data += remaining_line.strip()
        # 75 seems to be the line delimiter
        all_data = []
        longest_dataline = -1
        for dataline in image_data.split("75"):
            if dataline:

                dataline = "75" + dataline

                hex_formatted_dataline = "".join(get_chunks(dataline, 2))
                big_endian_hex_formatted_dataline = "".join(reversed(get_chunks(dataline, 2)))

                bin_formatted_dataline = "".join(get_binary_chunks(big_endian_hex_formatted_dataline, 2))
                if len(bin_formatted_dataline) > longest_dataline:
                    longest_dataline = len(bin_formatted_dataline)

                # # Add whitespace around some things
                # line_start = dataline[:2]
                #
                # # Line Length in hex (in half) (i.e. 8 bit word count)
                # line_length_in_hex = dataline[2:4]
                #
                # unknown_1 = dataline[4:8]
                #
                # remaining_dataline = " ".join(get_chunks(dataline[8:], 2))
                #
                # formatted_dataline = " ".join([line_start, line_length_in_hex, unknown_1, remaining_dataline])

                all_data.append(bin_formatted_dataline)
                hex_output.write(f"{hex_formatted_dataline}\n")
                big_endian_hex_output.write(f"{big_endian_hex_formatted_dataline}\n")
                bin_output.write(f"{bin_formatted_dataline}\n")
        print(len(all_data))

        all_data = ["e" * (longest_dataline - len(dl)) + dl for dl in all_data]
        bitmap = create_image_from_binary("".join(all_data), longest_dataline, len(all_data))
        bitmap.save(os.path.join(output_dir, "bitmap.bmp"))

        # create_ascii_image_from_binary("".join(all_data), longest_dataline, len(all_data))
