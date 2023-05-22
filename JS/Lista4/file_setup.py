import os
import subprocess

def file_setup():
    backup = "{0}/.backups".format(os.path.expanduser("~"))

    if "BACKUPS_DIR" in os.environ:
        backup = os.environ["BACKUPS_DIR"]
    if not os.path.exists(backup):
        subprocess.run(["mkdir", backup])

    json_file = "{0}/logs.json".format(backup)

    return backup, json_file
