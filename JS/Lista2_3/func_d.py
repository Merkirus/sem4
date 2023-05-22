from separate import separate
from input_to_string import *


def func_d(input):
    line_counter = 0
    image_counter = 0
    lines = input.split("\n")
    for line in lines:
        line_counter += 1
        words = separate(line)
        path = words[2][1]
        if (path.endswith(".gif") or path.endswith(".jpg") or path.endswith(".jpeg") or path.endswith(".xbm")):
            image_counter += 1
    print(f'Stosunek zdjęć: {image_counter/line_counter}')


if __name__ == "__main__":
    text = input_to_string()
    func_d(text)
