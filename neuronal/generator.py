#!/usr/bin/env python3

from pathlib import Path
import re
import math
import json

def euclidian_distance(list_a, list_b):
    sum = 0.0
    for i in range(len(list_a)):
        sum += (list_a[i] - list_b[i])**2
    return math.sqrt(sum)

def read_template(filename):
    with open(filename, 'r', encoding='UTF-8') as file:
        return file.readlines()

def read_queries(filename):
    with open(filename, 'r', encoding='UTF-8') as file:
        return file.read().split()

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

def fetch_embeddings(filename):
    embeddings_path = Path(filename + ".json")
    if embeddings_path.is_file():
        embeddings_file = open(filename + ".json")
        map = json.loads(embeddings_file.read())
        embeddings_file.close()
        return map
    else:
        return generate_embeddings(filename)

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

def generate_sentence(template, query, embeddings, lexicon):
    types = fetch_types(template)
    words = []
    blacklist = []
    matches = re.findall(r"\*\w+/(\w+)/(\w+)", template)
    for w1, w2 in matches:
        blacklist.append(w1)
        blacklist.append(w2)
    for type in types:
        word = find_best_word(lexicon[type], embeddings, query, blacklist)
        blacklist.append(word)
        words.append(word)
    sentence = str(template)
    parts_to_replace = re.findall(r"\*\w+(?:/\w+)?(?:/\w+)?", template)
    i = 0
    for p in parts_to_replace:
        sentence = sentence.replace(p, words[i])
        i += 1
    return sentence

def fetch_types(template):
    return re.findall(r"\*(\w+)(?:/\w+)?(?:/\w+)?", template)


def find_best_word(word_list, embeddings, query, blacklist):
    best_distance = float("inf")
    best_word = None
    for word in word_list:
        if word in blacklist:
            continue
        if word not in embeddings.keys():
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

for query in QUERIES:
    print(f"~ {query} ~")
    for sgp in TEMPLATE:
        print(generate_sentence(sgp, query, embeddings, lexicon), end="")
    print()
