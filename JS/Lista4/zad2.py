import os
import sys

def zad2(args):
    path_sep = os.pathsep
    folders = os.environ["PATH"].split(path_sep)
    for folder in folders:
        print("### "+folder+" ###")
        if len(args) == 0:
            continue
        if args[0] == "l":
            bins = os.listdir(folder)
            sep = os.sep
            na = [x for x in bins if os.path.isfile(folder+sep+x)]
            for bin in na:
                print(bin)
        print()


if __name__ == "__main__":
    parameters = sys.argv[1:]
    zad2(parameters)
