import pprint
import itertools
import json
import os.path
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')

def replacePunct(s):
    return [word.lower() for word in tokenizer.tokenize(s)]

def main(files, common_words):
    dict = {item[0].rstrip(): list(itertools.chain(*([replacePunct(line[1:])
                               for line in item[1:]
                               if line[0] in ["T", "W", "K"]])))
            for item in files}

    frequencies = {key: [(word, dict[key].count(word))
                         for word in dict[key]
                         if word not in common_words
                         ]
                   for key in dict}

    with open("C:/Users/corentin/Desktop/CACM/freq.json", "w") as export:
        export.write(json.dumps(frequencies, indent=4))
    return frequencies

def buildIndex():
    with open("C:/Users/corentin/Desktop/CACM/cacm.all", "r") as cacm:
        collection = cacm.read()
        with open("C:/Users/corentin/Desktop/CACM/common_words", "r") as cw:
            common_words  = replacePunct(cw.read())
            files = [item.split("\n.") for item in collection.split(".I ")]
            main(files, common_words)

def buildReversedIndex(frequencies):
    invertFreq = {}
    for key in frequencies:
        for freq in frequencies[key]:
            if freq[0] not in invertFreq:
                invertFreq[freq[0]] = [(key, freq[1])]
            else:
                invertFreq[freq[0]] += [(key, freq[1])]
    with open("C:/Users/corentin/Desktop/CACM/revertFreq.json", "w") as export:
        export.write(json.dumps(invertFreq, indent=4))
    return invertFreq



if __name__ == "__main__":
    if not os.path.isfile("C:/Users/corentin/Desktop/CACM/freq.json"):
        frequencies = buildIndex()
    else:
        with open("C:/Users/corentin/Desktop/CACM/freq.json", "r") as freq:
            frequencies = json.loads(freq.read())
    if not os.path.isfile("C:/Users/corentin/Desktop/CACM/revertFreq.json"):
        revertFreq = buildReversedIndex(frequencies)
    else:
        with open("C:/Users/corentin/Desktop/CACM/revertFreq.json", "r") as revF:
            revertFreq = json.loads(revF.read())