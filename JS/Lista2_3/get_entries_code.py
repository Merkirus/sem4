import sys
from read_log import read_log
from input_to_string import input_to_string
from print_entries import print_entries

def get_entries_code(input, code):
    it = filter(lambda x: str(x[6]) == code, input)
    result = list(it)
    return result


if __name__ == "__main__":
    text = input_to_string()
    krotki = read_log(text)
    try:
        filtered = get_entries_code(krotki, sys.argv[1])
        print_entries(filtered)
    except IndexError:
        print("Nieprawidlowa ilosc parametrow")
