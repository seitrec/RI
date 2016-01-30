##############################################################
# Name: Boolean
# Purpose: This module is designed to run vectorial queries on either CACM
#          or WIKI collection
# Author: Damien Peltier & Corentin Seitre
# Created: 12/15 - 01/16
##############################################################

import argparse
import operator
from parseCollection import replacePunct, count_words, loadJsons


def searchToQuery(search):
    #output : parsed query with words and occurence
    with open("../CACM/common_words", "r") as cw:
        common_words = replacePunct(cw.read())
        return count_words(common_words, search.split())

def get_documents_norms(ifreq):
    """
    To be used with either tfidf or tfidfnorm
    :param ifreq:
    :return:
    """
    weights_by_doc = {}
    for word, docs in ifreq.iteritems():
        for doc in docs:
            id = doc[0]
            weight = doc[1]
            if id in weights_by_doc:
                weights_by_doc[id] += [weight*weight]
            else:
                weights_by_doc[id] = [weight*weight]
    return {id: sum(value) for id, value in weights_by_doc.iteritems()}


def projectionQuery(words, ifreq):

    doc_norms = get_documents_norms(ifreq)
    #take parsed query as input and output the documents with their scores

    similarity = {}

    #computing the norm of the query
    norm_query_temp = 0
    for word in words:
        norm_query_temp += words[word]**2
    norm_query = norm_query_temp**(0.5)

    for word in words:
        wordstring = word
        word_weight = words[word]/norm_query #weight normalized
        if wordstring in ifreq:
            wordifreq = ifreq[wordstring]
            for document in wordifreq:
                id = document[0]
                norm_doc = doc_norms[id]**(0.5)
                doc_weight = document[1]/norm_doc #weight normalized
                if id in similarity.keys():
                    similarity[id] += doc_weight * word_weight
                else:
                    similarity[id] = doc_weight * word_weight
    sortedSimilarity = sorted(similarity.items(), key=operator.itemgetter(1), reverse=False)
    #for doc in sortedSimilarity:
      #  threshold = int(sortedSimilarity[-1][1]*0.5)
       # if doc[1]> threshold:
        #    print "Doc %s avec un score de %.2f" % (doc[0], doc[1])
    return sortedSimilarity


def main(collection, reverseType, query):
    words = searchToQuery(query)
    freq, ifreq = loadJsons(collection, reverseType, words)
    return projectionQuery(words, ifreq)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query CACM or WIKI and get vectorial results")
    parser.add_argument("-c", "--collection", default="CACM", help="The collection we want to query from")
    parser.add_argument("-q", "--query", default="ancient weapon", help="The words we want to search")
    parser.add_argument("-i", "--inverse", default="standard", help="The type of inverse freq index to use (standard, "
                                                                    "tfidf, tfidfnorm")
    args = parser.parse_args()

    main(args.collection, args.inverse, args.query)

