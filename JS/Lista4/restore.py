import os
import json
import sys
import subprocess
import datetime
from file_setup import file_setup

def restore(path):
    if len(path) == 0:
        path = os.getcwd()
    else:
        path = path[0]
    
    if not os.path.isdir(path):
        return

    _, json_file = file_setup()

    if not os.path.exists(json_file):
        return
    
    lstObj = []

    with open(json_file, "r") as out:
        try:
            lstObj = json.load(out)
        except json.JSONDecodeError:
            pass

    if len(lstObj) == 0:
        return

    def convert(x):
        date, hour, minute, second = x.split(":")
        year, month, day = date.split("-")
        return datetime.datetime.combine(datetime.date(int(year), int(month), int(day)), datetime.time(int(hour), int(minute), int(second)))

    lstObj.sort(key=lambda x: convert(x["date"]))

    for i in range(len(lstObj)):
        print(f"Index: {i}\n{lstObj[i]}")

    index = ""
    result = ""

    while True:
        print("Choose index of backup to unpack")
        index = input()
        try:
            index = int(index)
            result = lstObj.pop(index)
            break
        except ValueError:
            print("Wrong type")
            continue
        except IndexError:
            print("Wrong index")
            continue

    with open(json_file, "w") as out:
        json.dump(lstObj, out, indent=4)

    
    subprocess.run(["unzip", result["backup_path"], "-d", path])


if __name__ == "__main__":
    path = sys.argv[1:]
    restore(path)
