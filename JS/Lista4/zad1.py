import sys
import os

def zad1(args):
    if (len(args)) == 0:
        for key, value in os.environ.items():
            print(key, value)
        return
    result = []
    keywords = [x.lower() for x in args]
    for key, value in os.environ.items():
        for keyword in keywords:
            if key.lower().find(keyword) != -1:
                result.append((key, value))
                break
    result = sorted(result, key=lambda x: x[0])
    for entry in result:
        print(entry)


if __name__ == "__main__":
    parameters = sys.argv[1:]
    zad1(parameters)
