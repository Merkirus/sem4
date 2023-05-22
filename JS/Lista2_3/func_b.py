from input_to_string import *


def func_b(input):
    sum = 0
    lines = input.split("\n")
    for line in lines:
        words = line.split(" ")
        try:
            sum += int(words[-1])
        except ValueError:
            continue
    print(f'Suma gigabajtów: {sum/1_000_000_000} GB')


if __name__ == "__main__":
    text = input_to_string()
    func_b(text)
