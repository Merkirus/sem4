from separate import separate
from input_to_string import *


def func_c(input):
    path = ''
    max_bytes = -1
    lines = input.split("\n")
    for line in lines:
        words = separate(line)
        try:
            nr_of_bytes = int(words[-1])
            if (nr_of_bytes > max_bytes):
                max_bytes = nr_of_bytes
                http = words[2]
                path = http[1]
        except ValueError:
            continue
    print(f'Ścieżka: {path}')
    print(f'Bajty: {max_bytes}')


if __name__ == "__main__":
    text = input_to_string()
    func_c(text)
