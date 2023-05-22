import re


def separate(line):  # separates line into words - address, date, http request, code, bytes
    try:
        arr = line.split(" ")
        if (len(arr) > 10):
            raise IndexError  # bad line format
        address = arr[0]
        date = arr[3:5]
        date[0] = date[0].replace("[", "")
        date[-1] = date[-1].replace(']', "")
        http = arr[5:8]
        http[0] = http[0].replace('"', "")
        http[-1] = http[-1].replace('"', "")
        code = arr[8]
        byte = arr[9]
        return ([address, date, http, code, byte])
    except IndexError:
        return (["", ["-", "-"], ["-", "-", "-"], "-", "-"])
