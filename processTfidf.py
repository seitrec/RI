##############################################################
# Name: Tfidf
# Purpose: This modeule is designed to build tfidf indexes from
#          standard inverse frequency indexes and other usefull information
# Author: Damien Peltier & Corentin Seitre
# Created: 12/15 - 01/16
##############################################################

import math
import json
import os


def build_CACMtfidf(freq, ifreq):
    N = float(len(freq.keys()))
    tfidf = process_tfidf(ifreq, N)
    with open("../CACMindexes/revertFreqTfidf.json", "w") as export:
        export.write(json.dumps(tfidf, indent=2))
    return tfidf


def build_CACMNormtfidf(freq, tfidf):
    doc_lengths = {key: sum(value for word, value in doc.iteritems()) for key, doc in freq.iteritems()}
    tfidf = build_tfidf_norm(tfidf, doc_lengths)
    with open("../CACMindexes/revertFreqNormTfidf.json", "w") as export:
        export.write(json.dumps(tfidf, indent=2))
    return tfidf


def process_tfidf(ifreq, N):
    tfidfdict = {}
    for word in ifreq:
        tfidfdict[word] = [(doc[0], doc[1] * math.log(N / len(ifreq[word]))) for doc in ifreq[word]]
    return tfidfdict


def build_tfidf_norm(tfidf, doc_lengths):
    normtfidf = {}
    for word in tfidf:
        try:
            normtfidf[word] = [(id, freq / doc_lengths[id]) for id, freq in tfidf[word]]
        except (KeyError):
            pass
    return normtfidf


def build_WIKItfidf():
    N = 660000
    for j, filename in enumerate(os.listdir("../WIKIindexes/finalWiki/")):
        print(j)
        with open("../WIKIindexes/finalWiki/" + filename, "r") as f:
            ifreq = json.loads(f.read())
            tfidf = process_tfidf(ifreq, N)
        with open("../WIKIindexes/finalWikiTfidf/" + filename, "w") as export:
            export.write(json.dumps(tfidf, indent=2))


def build_WIKItfidfNorm(doc_lengths):
    for j, filename in enumerate(os.listdir("../WIKIindexes/finalWikiTfidf/")):
        print(j)
        with open("../WIKIindexes/finalWikiTfidf/" + filename, "r") as f:
            tfidf = json.loads(f.read())
            tfidf = build_tfidf_norm(tfidf, doc_lengths)
        with open("../WIKIindexes/finalWikiTfidfNorm/" + filename, "w") as export:
            export.write(json.dumps(tfidf, indent=2))


if __name__ == "__main__":
    build_WIKItfidf()
    build_WIKItfidfNorm()
