from separate import *
from input_to_string import input_to_string


def func_h(input):
    result = ""
    lines = input.split("\n")
    for line in lines:
        words = separate(line)
        address = words[0]
        if (address.endswith(".pl")):
            result += (line + "\n")
    print(result.rstrip(result[-1]), end="")


if __name__ == "__main__":
    text = input_to_string()
    func_h(text)
