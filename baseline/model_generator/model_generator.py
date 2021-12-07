#!/usr/bin/env python3

import sys
import re
from pathlib import Path
import time
import json
import os

def get_file_list(folder):
    file_list = []
    for file in list(Path(folder).rglob("*.pdf.seg")):
        file_list.append(str(file))
    return file_list

def file_to_string(filename):
    data = ""
    with open(filename, 'r') as file:
        data = file.read().replace('\n', ' ')
    return data

def remove_punctuation(text):
    text = re.sub(("[^\wÀ-ÿ'’]"), " ", text)
    text = text.replace("_", " ")
    text = re.sub('\s{2,}| {2,}', " ", text)
    return text

# if pair in list and key = arg return true
def in_pair_of_list(value, l):
    for pair in l:
        if pair[0] == value:
            return True
    return False

def save_dictionnary_in_file(dictionnary, filename):
    first = True
    with open(filename, "w", encoding="UTF-8") as file:
        for key in dictionnary:
            line = ""
            value = dictionnary[key]
            if not first:
                line = "\n"
            line += str(key) + " : " + str(value)
            first = False
            file.write(line)

def save_json_dictionnary_in_file(dictionnary, filename):
    file = open(filename, "w", encoding="utf-8")
    # json.dump(dictionnary, file, ensure_ascii=False)
    file.write(json.dumps(dictionnary, ensure_ascii=False))
    file.close()

folder = sys.argv[1]
n = int(sys.argv[2])
output = sys.argv[3]

# Check if correct options
if n != 2 and n != 3:
    print("ERROR: n parameter must be 2 or 3!")
    exit()

# Calculate frequency map
file_list = get_file_list(folder)
frequency_map = dict()
start_time = time.time()
size_count = 0
for file in file_list:
    print("Processing file " + file + "...", end="")
    size_count = size_count + os.path.getsize(file)
    text = file_to_string(file).lower()
    sentences = text.split("\n")
    for sentence in sentences:
        sentence = remove_punctuation(sentence)
        words = sentence.split(" ")
        words.remove("")
        for i in range(1, len(words) - (n - 1)):
            ngram = ()
            if n == 2:
                ngram = (words[i], words[i + 1])
            elif n == 3:
                ngram = (words[i], words[i + 1], words[i + 2])
            left = words[i]
            right = words[i+1]
            if ngram not in frequency_map:
                frequency_map[ngram] = 0
            frequency_map[ngram] = frequency_map[ngram] + 1
    print(" " + str(size_count / (1000*1000)) + "MB")

print("Sorting frequency map...", end = "")
frequency_map = dict(sorted(frequency_map.items(), key = lambda item: item[1]))
print(" DONE")

# save_dictionnary_in_file(frequency_map, "tmp_output.txt")

print("Calculating frequency map...", end = "")
model_map = dict()
for ngram, frequency in frequency_map.items():
    if n == 2:
        model_map[ngram[0]] = (ngram[1])
    elif n == 3:
        model_map[ngram[0]] = (ngram[1], ngram[2])
print(" DONE")
    
print("Took %s seconds" % (time.time() - start_time))
save_json_dictionnary_in_file(model_map, output)
