import os
import json
import sys
import subprocess
import datetime
from file_setup import file_setup

def backup(path):
    if len(path) == 0:
        return
    
    path = path[0]

    if not os.path.isdir(path):
        return

    backup, json_file = file_setup()

    if not os.path.exists(json_file):
        subprocess.run(["touch", json_file])

    date = datetime.datetime.now().strftime("%Y-%m-%d:%H:%M:%S")
    file_name = "{0}-{1}.zip".format(date, os.path.basename(path))
    subprocess.run(["zip", "-r",  file_name, path])
    subprocess.run(["mv", file_name, "{0}/{1}".format(backup, file_name)])

    lstObj = []

    with open(json_file, "r") as out:
        try:
            lstObj = json.load(out)
        except json.JSONDecodeError:
            pass

    new_rec = {
           "date": str(date),
            "path": str(path),
            "backup_path": "{0}/{1}".format(backup, file_name)
            }

    lstObj.append(new_rec)

    with open(json_file, "w") as out:
        json.dump(lstObj, out, indent=4)


if __name__ == "__main__":
    path = sys.argv[1:]
    backup(path)
