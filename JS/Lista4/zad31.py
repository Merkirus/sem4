from collections import defaultdict
import json
import sys

def zad31(path):
    line_counter = 0
    word_counter = 0
    char_counter = 0
    chars = defaultdict(lambda: 0)
    words = defaultdict(lambda: 0)
    with open(path) as p:
        for line in p:
            line_counter += 1
            line = line.rstrip()
            ls_chars = list(line)
            ls_words = line.split(" ")
            char_counter += len(ls_chars)
            for char in ls_chars:
                chars[char] = chars[char] + 1
            word_counter += len(ls_words)
            for word in ls_words:
                words[word] = words[word] + 1
        most_freq_word = max(words, key=words.get)
        most_freq_char = max(chars, key=chars.get)
        to_json = {
                "Lines": line_counter,
                "Words": word_counter,
                "Characters": char_counter,
                "Most frequent character": most_freq_char,
                "Most frequent word": most_freq_word
                }
        print(json.dumps(to_json))

    

if __name__ == "__main__":
    path = sys.argv[1:]
    zad31(path[0])
