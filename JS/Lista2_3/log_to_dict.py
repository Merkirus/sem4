from entry_to_dict import entry_to_dict
from print_dict_entry_dates import print_dict_entry_dates
from input_to_string import input_to_string
from read_log import read_log

def log_to_dict(input):
    result = []
    for krotka in input:
        result.append(entry_to_dict(krotka))
    result_dict = {}
    for record in result:
        for key, value in record.items():
            if key == "domain":
                result_dict[value] = []
    for record in result:
        result_dict[record["domain"]].append(record)
    return result_dict


if __name__ == "__main__":
    text = input_to_string()
    krotki = read_log(text)
    ls = log_to_dict(krotki)
    print_dict_entry_dates(ls)
