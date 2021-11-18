#!/usr/bin/env python3

import sys      # argv,
import json     # loads,
import random   # randint,

LANG_MODEL_FILENAME = sys.argv[1]
DESIRED_SENTENCE_LENGTH = int(sys.argv[2])

FIRST_WORDS_FILENAME = 'first_words.json'

# return python object matching json
def load_json(filename: str):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.loads(file.read())

# # return str
# def get_starting_word(d: dict):
#     return random.choice(list(d.keys()))

def get_random_key(dictionnary):
    return random.choice(list(dictionnary.keys()))

# return list of str
def get_next_words(word: str, d: dict):
    if isinstance(d[word], str):
        return [d[word]]
    return d[word]

model = load_json(LANG_MODEL_FILENAME)
starting_word = get_random_key(model)
sentence = [starting_word]

while len(sentence) < DESIRED_SENTENCE_LENGTH:
    last_word = sentence[len(sentence) - 1]
    sentence.extend(get_next_words(last_word, model))

print(sentence[:DESIRED_SENTENCE_LENGTH])