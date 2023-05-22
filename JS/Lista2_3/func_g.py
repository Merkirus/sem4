from separate import separate
from input_to_string import input_to_string
from datetime import *


def func_g(input):
    result = ""
    lines = input.split("\n")
    for line in lines:
        words = separate(line)
        whole_date = words[1][0]
        try:
            day, month, year = whole_date[:whole_date.find(":")].split("/")
            datetime_object = datetime.strptime(month, "%b")
            month = datetime_object.month
            dt = date(int(year), month, int(day))
            if (dt.weekday() == 4):
                result += (line + "\n")
        except ValueError:  # Pattern matching may give ValueError if given bad format and date() as well
            continue
    print(result.rstrip(result[-1]), end="")


if __name__ == "__main__":
    text = input_to_string()
    func_g(text)
