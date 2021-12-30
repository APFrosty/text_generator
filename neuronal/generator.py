#!/usr/bin/env python3

from os import set_inheritable
from pathlib import Path
import re
import math
import json
from difflib import SequenceMatcher

# Measure the euclidian distance between two points
def euclidian_distance(list_a, list_b):
    sum = 0.0
    for i in range(len(list_a)):
        sum += (list_a[i] - list_b[i])**2
    return math.sqrt(sum)

# Return list of templates from a template file
def read_template(filename):
    with open(filename, 'r', encoding='UTF-8') as file:
        return file.readlines()

# Return list or queries from a file
def read_queries(filename):
    with open(filename, 'r', encoding='UTF-8') as file:
        return file.read().split()

# Generate an embedding map from a .txt file and stores it in a file before returning the map
def generate_embeddings(filename):
    map = {}
    file = open(filename)
    for line in file.readlines():
        line = line.replace('[', '')
        line = line.replace(']', '')
        line = line.replace(',', ' ')
        i = -1
        word = ""
        position = []
        for element in line.split():
            if i == -1:
                word = element
            else:
                position.append(float(element))
            i += 1
        map[word] = position
    file.close()
    saved_dict = open(filename + ".json", "w")
    json.dump(map, saved_dict)
    saved_dict.close()
    return map

# Check if embedding cache exist and if so generate a map from it and if not generate an embedding map
def fetch_embeddings(filename):
    embeddings_path = Path(filename + ".json")
    if embeddings_path.is_file():
        embeddings_file = open(filename + ".json")
        map = json.loads(embeddings_file.read())
        embeddings_file.close()
        return map
    else:
        return generate_embeddings(filename)

# Generate lexicon map<grammatical strucuture, list of words> from a file
def generate_lexicon(filename):
    map = {}
    file = open(filename)
    for line in file.readlines():
        line = line.replace('[', '')
        line = line.replace(']', '')
        line = line.replace(',', ' ')
        i = -1
        key = ""
        words = []
        for element in line.split():
            if i == -1:
                key = element
            else:
                words.append(element)
            i += 1
        map[key] = words
    file.close()
    return map

# Generate a sentence from a template, a query, an embedding map and a lexicon map
# Each used word is blacklisted to avoid using the same word twice
# Each word already in the SGP template are blacklisted
# We check if the word must start with a vowel, a consonant, or if such consideration is not required
def generate_sentence(template, query, embeddings, lexicon):
    types = fetch_types(template)
    words = []
    blacklist = []
    matches = re.findall(r"\*\w+/(\w+)/(\w+)", template)
    previous = re.findall(r"(\w+'?) \*\w+/(?:\w+)/(?=\w+)", template)
    i = 0
    for w1, w2 in matches:
        blacklist.append(w1)
        blacklist.append(w2)
    for type in types:
        start_with_vowel = previous[i].endswith("'")
        start_with_consonant = previous[i].lower() == "de" or previous[i].lower() == "le" or previous[i].lower() == "la" or previous[i].lower().endswith("_de") or previous[i].lower().endswith("_le") or previous[i].lower().endswith("_la")
        word = find_best_word(lexicon[type], embeddings, query, blacklist, start_with_vowel, start_with_consonant)
        blacklist.append(word)
        words.append(word)
        i += 1
    sentence = str(template)
    parts_to_replace = re.findall(r"\*\w+(?:/\w+)?(?:/\w+)?", template)
    i = 0
    for p in parts_to_replace:
        first_word = sentence.startswith(p)
        word = words[i]
        if(first_word):
            word[i] = word[i].upper()
        else:
            word = word.lower()    
        sentence = sentence.replace(p, word)
        i += 1
    return sentence

# Retrieve the grammatical types that exist in the given template
def fetch_types(template):
    return re.findall(r"\*(\w+)(?:/\w+)?(?:/\w+)?", template)

# Check if the given character is a vowel
def is_vowel(character):
    vowels = ["a", "e", "i", "o", "u", "y"]
    return character.lower() in vowels

# Find the word closest to the query from a list of word
# Words can be blacklisted, can require starting with a vowel, can require starting with a consonant
def find_best_word(word_list, embeddings, query, blacklist, start_with_vowel, start_with_consonant):
    best_distance = float("inf")
    best_word = None
    for word in word_list:
        if word not in embeddings.keys():
            continue
        if word in blacklist:
            continue
        if start_with_vowel and is_vowel(word[0]) == False:
            continue
        if start_with_consonant and is_vowel(word[0]):
            continue
        for blacklisted in blacklist:
            ratio = SequenceMatcher(None, word, blacklisted).ratio()
            if ratio > 0.9:
                continue
        if best_word == None:
            best_word = word
            best_distance = euclidian_distance(embeddings[query], embeddings[word])
            continue
        distance = euclidian_distance(embeddings[query], embeddings[word])
        if distance < best_distance:
            best_word = word
            best_distance = distance
    return best_word

TEMPLATE = read_template("resources/templates_sgp.txt")
QUERIES = read_queries("resources/queries.txt")
embeddings = fetch_embeddings("resources/embeddings-Fr.txt")
lexicon = generate_lexicon("resources/TableAssociative.txt")

# For each pair of query/sgp, we generate a sentence
for query in QUERIES:
    print(f"~ {query} ~")
    for sgp in TEMPLATE:
        print(generate_sentence(sgp, query, embeddings, lexicon), end="")
    print()
