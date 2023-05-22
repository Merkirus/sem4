from read_log import read_log
from input_to_string import input_to_string
import sys
from operator import itemgetter
from print_entries import print_entries

def sort_log(input, flag):
    try:
        return input.sort(key = lambda x: x[flag])
    except IndexError:
        return input
    return input


if __name__ == "__main__":
    text = input_to_string()
    krotki = read_log(text)
    try:
        index = int(sys.argv[1])
        krotki = sorted(krotki, key=itemgetter(index))
        print_entries(krotki)
    except TypeError:
        print("Nie podano liczby")
    except IndexError:
        print("Nie podano parametru")
