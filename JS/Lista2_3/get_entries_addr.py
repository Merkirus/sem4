import sys
from read_log import read_log
from input_to_string import input_to_string
from operator import itemgetter
from print_entries import print_entries

def get_entries_addr(input, host, code):
    it = filter(lambda x: x[0] == host, input)
    result = list(it)
    print(result)
    it = filter(lambda x: str(x[6]) == code, result)
    result = list(it)
    return result


if __name__ == "__main__":
    text = input_to_string()
    krotki = read_log(text)
    try:
        filtered = get_entries_addr(krotki, sys.argv[1], sys.argv[2])
        print_entries(filtered)
    except IndexError:
        print("Nieprawidlowa ilosc parametrow")
