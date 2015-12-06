from main import *
import operator


def searchToQuery(search):
    common_words = import_cw()
    return count_words(common_words, search.split())


def projectionQuery(words,ifreq):
    similarity = {}
    for word in words:
        wordstring = word[0]
        word_weight = word[1]
        if wordstring in ifreq.keys():
            wordifreq = ifreq[wordstring]
            for document in wordifreq:
                id = document[0]
                weight = document[1]
                if id in similarity.keys():
                    similarity[id] += weight*word_weight
                else:
                    similarity[id] = weight*word_weight
    sortedSimilarity = sorted(similarity.items(), key=operator.itemgetter(1), reverse=True)
    for doc in sortedSimilarity:
        print "Doc %s avec un score de %d" % (doc[0], doc[1])


if __name__ == "__main__":
    freq, ifreq = loadJsons()
    projectionQuery(searchToQuery("error"), ifreq)


