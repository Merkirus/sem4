from input_to_string import input_to_string
from read_log import read_log
from log_to_dict import log_to_dict

def get_addr(input):
    result = []
    for key in input.keys():
        result.append(key)
    return result


if __name__ == "__main__":
    text = input_to_string()
    krotki = read_log(text)
    ls = log_to_dict(krotki)
    addr = get_addr(ls)
    for a in addr:
        print(a)
