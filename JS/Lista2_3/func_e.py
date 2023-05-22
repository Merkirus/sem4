from separate import separate
from input_to_string import input_to_string


def func_e(input):
    result = ""
    lines = input.split("\n")
    for line in lines:
        words = separate(line)
        code = words[-2]
        if (code == "200"):
            result += (line + "\n")
    print(result.rstrip(result[-1]), end="")


if __name__ == "__main__":
    text = input_to_string()
    func_e(text)
