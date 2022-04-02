def get_chunks(a_str, chunk_size):
    return [a_str[i:i + chunk_size] for i in range(0, len(a_str), chunk_size)]


def swap_endianness(image_line: str) -> str:
    return "".join(reversed(get_chunks(image_line, 2)))
