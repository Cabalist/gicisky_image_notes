
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

def get_chunks(a_str, chunk_size):
    return [a_str[i:i + chunk_size] for i in range(0, len(a_str), chunk_size)]


def swap_endianness(image_line: str) -> str:
    return "".join(reversed(get_chunks(image_line, 2)))


