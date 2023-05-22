import sys
from read_log import read_log
from input_to_string import input_to_string
from print_entries import print_entries

def get_failed_read(input, flag):
    it = filter(lambda x: str(x[6]).startswith("4"), input)
    http4 = list(it)
    it = filter(lambda x: str(x[6]).startswith("5"), input)
    http5 = list(it)
    if flag == "y":
        return http4 + http5
    return http4, http5


if __name__ == "__main__":
    text = input_to_string()
    krotki = read_log(text)
    try:
        flag = sys.argv[1].lower()
        print(flag)
        if flag != "y" and flag != "n":
            raise Exception("Nie podano odpowiedniej flagi logicznej")
        result = []
        result2 = []
        if flag == "y":
            result = get_failed_read(krotki, flag)
            print_entries(result)
        else:
            result, result2 = get_failed_read(krotki, flag)
            print_entries(result)
            print_entries(result2)
    except Exception as e:
        print(e)
