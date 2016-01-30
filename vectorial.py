##############################################################
# Name: Boolean
# Purpose: This modeule is designed to run vectorial queries on either CACM
#          or WIKI collection
# Author: Damien Peltier & Corentin Seitre
# Created: 12/15 - 01/16
##############################################################

import argparse
import operator
from parseCollection import replacePunct, count_words, loadJsons, buildFrequencies


def searchToQuery(search):
    with open("../CACM/common_words", "r") as cw:
        common_words = replacePunct(cw.read())
        return count_words(common_words, search.split())


def projectionQuery(words, ifreq):
   # print words, ifreq
    similarity = {}
    for word in words:
        wordstring = word
        word_weight = words[word]
        if wordstring in ifreq:
            wordifreq = ifreq[wordstring]
            for document in wordifreq:
                id = document[0]
                weight = document[1]
                if id in similarity.keys():
                    similarity[id] += weight * word_weight
                else:
                    similarity[id] = weight * word_weight
    sortedSimilarity = sorted(similarity.items(), key=operator.itemgetter(1), reverse=False)
    #for doc in sortedSimilarity:
     #   threshold = int(sortedSimilarity[-1][1]*0.5)
      #  if doc[1]> threshold:
       #     print "Doc %s avec un score de %d" % (doc[0], doc[1])
    return sortedSimilarity


def main(collection, query):
    words = searchToQuery(query)
    freq, ifreq = loadJsons(collection, "tfidf", words)
    return projectionQuery(words, ifreq)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query CACM or WIKI and get vectorial results")
    parser.add_argument("-c", "--collection", default="CACM", help="The collection we want to query from")
    parser.add_argument("-q", "--query", default="error system", help="The words we want to search")
    args = parser.parse_args()

    main(args.collection, args.query)
