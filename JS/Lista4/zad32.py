import sys
import os
import subprocess
import json
from collections import defaultdict

def zad32(path):
    if not os.path.isdir(path):
        return
    files = os.listdir(path)
    files = [x for x in files if os.path.isfile(path+os.sep+x)]
    results = []
    for file in files:
        result = subprocess.run(["python", "zad31.py", path+os.sep+file], capture_output=True)
        new_dict = json.loads(result.stdout.decode('utf-8'))
        results.append(new_dict)
    final_results = defaultdict(lambda: 0)
    char_helper = defaultdict(lambda: 0)
    word_helper = defaultdict(lambda: 0)
    for d in results:
        for key, value in d.items():
            try:
                final_results[key] = final_results[key] + int(value)
            except ValueError:
                if len(value) > 1:
                    word_helper[value] = word_helper[value] + 1
                else:
                    char_helper[value] = char_helper[value] + 1
    final_results["Most frequent character"] = max(char_helper, key=char_helper.get)
    final_results["Most frequent word"] = max(word_helper, key=word_helper.get)
    print(f"Number of files: {len(files)}")
    for key, value in final_results.items():
        print(f"{key}, '{value}'")


if __name__ == "__main__":
    path = sys.argv[1:]
    zad32(path[0])
