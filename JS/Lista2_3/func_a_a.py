from separate import separate
from input_to_string import *


def func_a_a(input):
    counter = 0
    lines = input.split('\n')
    for line in lines:
        words = separate(line)
        if (words[-2] == "200"):
            counter += 1
    print(f'Liczba żądań z kodem 200: {counter}')


if __name__ == "__main__":
    text = input_to_string()
    func_a_a(text)
