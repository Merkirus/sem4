from input_to_string import input_to_string
from read_log import read_log

def entry_to_dict(krotka):
    d = {
        "domain": krotka[0],
        "date": krotka[1],
        "request": " ".join(krotka[3:6]),
        "code": krotka[6],
        "bytes": krotka[7]}
    return d


if __name__ == "__main__":
    text = input_to_string()
    krotki = read_log(text)
    result = []
    for krotka in krotki:
        result.append(entry_to_dict(krotka))
    for dict_ent in result:
        print(dict_ent)
