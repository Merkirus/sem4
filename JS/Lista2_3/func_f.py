from separate import separate
from input_to_string import *


def func_f(input):
    result = ""
    lines = input.split("\n")
    for line in lines:
        words = separate(line)
        date = words[1][0]
        try:
            full_date = date.split(":")
            hour = full_date[1]
            hour = int(hour)
            if (hour < 6 or hour >= 22):
                result += (line + "\n")
        except IndexError:  # bad format - date:hour:minute:second not found
            continue
        except ValueError:  # hour - bad value given in hour
            continue
    print(result.rstrip(result[-1]), end="")


if __name__ == "__main__":
    text = input_to_string()
    func_f(text)
