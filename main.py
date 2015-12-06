import pprint
import itertools
import json
import os.path
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')


def replacePunct(s):
    return [word.lower() for word in tokenizer.tokenize(s)]


def count_words(common_words, list_words):
    return [(word, list_words.count(word))
            for word in list_words
            if word not in common_words
            ]


def import_cw():
    with open("../CACM/common_words", "r") as cw:
            return replacePunct(cw.read())


def buildIndex():
    with open("../CACM/cacm.all", "r") as cacm:
        collection = cacm.read()
        common_words = import_cw()
        files = [item.split("\n.") for item in collection.split(".I ")]
        main(files, common_words)


def main(files, common_words):
    dict = {item[0].rstrip(): list(itertools.chain(*([replacePunct(line[1:])
                                                      for line in item[1:]
                                                      if line[0] in ["T", "W", "K"]])))
            for item in files}

    frequencies = {key: count_words(common_words, dict[key])
                   for key in dict}

    with open("../CACM/freq.json", "w") as export:
        export.write(json.dumps(frequencies, indent=4))
    return frequencies


def buildReversedIndex(frequencies):
    invertFreq = {}
    for key in frequencies:
        for freq in frequencies[key]:
            if freq[0] not in invertFreq:
                invertFreq[freq[0]] = [(key, freq[1])]
            else:
                invertFreq[freq[0]] += [(key, freq[1])]
    with open("../CACM/revertFreq.json", "w") as export:
        export.write(json.dumps(invertFreq, indent=4))
    return invertFreq


def loadJsons():
    if not os.path.isfile("../CACM/freq.json"):
        frequencies = buildIndex()
    else:
        with open("../CACM/freq.json", "r") as freq:
            frequencies = json.loads(freq.read())
    if not os.path.isfile("../CACM/revertFreq.json"):
        revertFreq = buildReversedIndex(frequencies)
    else:
        with open("../CACM/revertFreq.json", "r") as revF:
            revertFreq = json.loads(revF.read())
    return frequencies, revertFreq


if __name__ == "__main__":
    loadJsons()
