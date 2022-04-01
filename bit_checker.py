from pathlib import Path



def check_if_40_is_always_the_fifth_and_sixth_bit():
    # Yes
    for each_dir in Path("successful_img_captures").iterdir():
        if not each_dir.is_dir():
            continue
        with open(each_dir / "formatted_image_data.hex") as f:
            for i, each_line in enumerate(f, start=1):
                if each_line[4:6] != "40":
                    print(f"{each_dir} :: Line {i} :: {each_line[4:6]}")


def check_if_80_is_always_the_thirteenth_and_fourteenth_bit():
    # No
    for each_dir in Path("successful_img_captures").iterdir():
        if not each_dir.is_dir():
            continue
        with open(each_dir / "formatted_image_data.hex") as f:
            for i, each_line in enumerate(f, start=1):
                if each_line[12:14] != "80":
                    print(f"{each_dir} :: Line {i} :: {each_line[12:14]}")


def is_seventh_and_eight_bit_always_multiple_of_0x10():
    # Yes
    all_bytes = set()
    for each_dir in Path("successful_img_captures").iterdir():
        if not each_dir.is_dir():
            continue
        with open(each_dir / "formatted_image_data.hex") as f:
            for i, each_line in enumerate(f, start=1):
                all_bytes.add(each_line[6:8])
                # if each_line[6:8] != "80":
                #     print(f"{each_dir} :: Line {i} :: {each_line[12:14]}")
    print(list(sorted(all_bytes)))

if __name__ == "__main__":
    # check_if_40_is_always_the_fifth_and_sixth_bit()
    is_seventh_and_eight_bit_always_multiple_of_0x10()