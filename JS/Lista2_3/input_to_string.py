import sys


def input_to_string():
    output = ''
    for line in sys.stdin:
        output += line
    return output
