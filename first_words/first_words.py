#!/usr/bin/env python3

from pathlib import Path
import re
import sys
import json

def get_file_list(folder):
    file_list = []
    for file in list(Path(folder).rglob("*.pdf.seg")):
        file_list.append(str(file))
    return file_list

def file_to_string(filename):
    data = ""
    with open(filename, 'r') as file:
        data = file.read()
    return data

INPUT_DIR = sys.argv[1]
OUTPUT_FILE = 'first_words.json'

file_list = get_file_list(INPUT_DIR)
first_words = set()

for filename in file_list:
    text = file_to_string(filename)
    text = re.sub(("[^\w,\.À-ÿ'’]"), " ", text)
    text = re.sub(("\d"), " ", text)
    text = text.replace("_", " ")
    words_after_punc = re.findall(r'(?:,|\.|;)\s+(\w+)\s+', text, re.UNICODE)
    for match in words_after_punc:
        first_words.add(match.lower())

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write(json.dumps(list(first_words), ensure_ascii=False))
