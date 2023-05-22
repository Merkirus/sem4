from separate import separate
from input_to_string import input_to_string
import datetime


def read_log(input):
    lines = input.split("\n")
    arr_lines = []
    for line in lines:
        words = separate(line)
        if words == ["", ["-", "-"], ["-", "-", "-"], "-", "-"]:
            continue
        address, full_date, http, code, byte = words
        date, some_number = full_date
        get, path, http_10 = http
        try:
            code = int(code)
            byte = int(byte)
            day, month, year = date[:date.find(":")].split("/")
            _, hour, minute, second = date[date.find(":"):].split(":")
            datetime_object = datetime.datetime.strptime(month, "%b")
            month = datetime_object.month
            dt = datetime.date(int(year), month, int(day))
            t = datetime.time(int(hour), int(minute), int(second))
            full_date = datetime.datetime.combine(dt, t)
            arr_lines.append((address, full_date, some_number, get, path, http_10, code, byte))
        except ValueError:
            arr_lines.append((address, datetime.datetime.combine(datetime.date(1,1,1), datetime.time(1,1,1)), some_number, get, path, http_10, 0, 0))
        except TypeError:
            arr_lines.append((address, datetime.datetime.combine(datetime.date(1,1,1), datetime.time(1,1,1)), some_number, get, path, http_10, 0, 0))
    #  print(arr_lines, end="")
    return arr_lines


if __name__ == "__main__":
    text = input_to_string()
    read_log(text)

