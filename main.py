import pprint
import itertools
import json
import os.path
from nltk.tokenize import RegexpTokenizer
from tfidf import *

tokenizer = RegexpTokenizer(r'\w+')


def replacePunct(s):
    """
    Parse a string into a list of words and removes punctuation and capital letters
    :param s: (str) string to parse
    :return: list of parsed words from s
    """
    return [word.lower() for word in tokenizer.tokenize(s)]


def count_words(common_words, string):
    """
    Count the meaningfull words in a string
    :param common_words (iterator): list of stopwords
    :param string: string to parse and count
    :return: (dict) word: occurences
    """
    dict = {}
    for word in string:
        if word not in common_words:
            if word not in dict:
                dict[word] = 1
            else:
                dict[word] += 1
    return dict


def buildFrequencies(files, common_words):
    """
    Count and order the occurences of the words in the CACM collection
    :param files: CACM collection
    :param common_words: dictionary of stop words (not to be taken into account)
    :return frequencies: (dict) doc_id: {word: frequency}
    """
    parts = {item[0].rstrip(): list(itertools.chain(*([replacePunct(line[1:])
                                                       for line in item[1:]
                                                       if line[0] in ["T", "W", "K"]])))
             for item in files}

    frequencies = {key: count_words(common_words, parts[key])
                   for key in parts}

    with open("../CACM/freq.json", "w") as export:
        export.write(json.dumps(frequencies, indent=4))
    return frequencies


def buildCACMIndex():
    """
    Build the term frequencies index for the CACM collection
    :return frequencies: (dict) doc_id: {word: frequency}
    """
    with open("../CACM/cacm.all", "r") as cacm:
        collection = cacm.read()
        with open("../CACM/common_words", "r") as cw:
            common_words = replacePunct(cw.read())
            files = [item.split("\n.") for item in collection.split(".I ")]
            return buildFrequencies(files, common_words)


def buildCACMReversedIndex(frequencies):
    """
    Build the reversed frequencies index for the CACM collection
    :param frequencies: (dict) frequencies dictionary for the CACM collection {doc_id: {word: frequency}}
    :return: invertFreq: (dict)
    """
    invertFreq = {}
    for key in frequencies:
        for word in frequencies[key]:
            if word not in invertFreq:
                invertFreq[word] = [(key, frequencies[key][word])]
            else:
                invertFreq[word] += [(key, frequencies[key][word])]
    with open("../CACM/revertFreq.json", "w") as export:
        export.write(json.dumps(invertFreq, indent=4))
    return invertFreq


def loadCACMJsons(reverseType):
    """
    Load/Build if necessary CACM indexes
    :param reverseType: (string) standard for occurences,
                                 tfidf for occurences*idf,
                                 tfidfnorm for occurences*idf/nbwords
    :return frequencies: (dict) doc_id: {word: occurences]
    :return revert_freq: (dict) word: doc occurencies (standard, tfidf, or tfidfnorm
    """
    frequencies, revert_freq = {}, {}
    if not os.path.isfile("../CACM/freq.json"):
        frequencies = buildCACMIndex()
    else:
        with open("../CACM/freq.json", "r") as freq:
            frequencies = json.loads(freq.read())
    if reverseType == "standard":
        if not os.path.isfile("../CACM/revert_freq.json"):
            revert_freq = buildCACMReversedIndex(frequencies)
        else:
            with open("../CACM/revert_freq.json", "r") as revF:
                revert_freq = json.loads(revF.read())
    elif reverseType == "tfidf":
        if not os.path.isfile("../CACM/revertFreqTfidf.json"):
            revert_freq = build_CACMtfidf()
        else:
            with open("../CACM/revertFreqTfidf.json", "r") as revF:
                revert_freq = json.loads(revF.read())
    elif reverseType == "tfidfnorm":
        if not os.path.isfile("../CACM/revertFreqNormTfidf.json"):
            revert_freq = build_CACMNormtfidf()
        else:
            with open("../CACM/revertFreqNormTfidf.json", "r") as revF:
                revert_freq = json.loads(revF.read())
    return frequencies, revert_freq


def loadWIKIJsons(words, reverseType):
    """We consider here that wiki indexes are already done. We're not going to build them on the go anyways"""
    with open("../Finalwiki/countWords.json", "r") as freq:
        frequencies = json.loads(freq.read())
    print('Loading indexes')
    revertFreq = {}
    try:
        for word in words:
            with open("../FinalwikiTfidf/" + word[0] + ".json", "r") as revF:
                part = json.loads(revF.read())
                revertFreq.update(part)
    except IOError:
        print "missing indexes"
    return frequencies, revertFreq


def loadJsons(collection, reverseType, words):
    """
    Load the necessary indexes for CACM or WIKI collections
    :param collection: (str) the used collection = "CACM" or "WIKI"
    :param reverseType: (string) standard for occurences,
                                 tfidf for occurences*idf,
                                 tfidfnorm for occurences*idf/nbwords
    :param words: requested words (for WIKI collection, we need to target loaded indexes on requested words)
    :return freq, ifreq: (dicts) frequencies and inverse frequencies dictionaries requested
    """
    if collection == "CACM":
        return loadCACMJsons(reverseType)
    if collection == "WIKI":
        return loadWIKIJsons(words, reverseType)


if __name__ == "__main__":
    freq, ifreq = loadJsons("CACM", "standard", [])
    freq, ifreq = loadJsons("CACM", "tfidf", [])
    freq, ifreq = loadJsons("CACM", "tfidfnorm", [])
