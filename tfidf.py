import argparse
import math
from main import *


def build_CACMtfidf():
    freq, ifreq = loadCACMJsons("standard")
    N = float(len(freq.keys()))
    tfidf = process_tfidf(ifreq, N)
    with open("../CACM/revertFreqTfidf.json", "w") as export:
        export.write(json.dumps(tfidf, indent=2))
    return tfidf


def build_CACMNormtfidf():
    freq, tfidf = loadCACMJsons("tfidf")
    doc_lengths = {key: sum(value for word, value in doc.iteritems()) for key, doc in freq.iteritems()}
    tfidf = build_tfidf_norm(tfidf, doc_lengths)
    with open("../CACM/revertFreqNormTfidf.json", "w") as export:
        export.write(json.dumps(tfidf, indent=2))
    return tfidf


def build_WIKItfidf():
    N = 660000
    for j, filename in enumerate(os.listdir("../finalWiki/")):
        print(j)
        with open("../finalWiki/" + filename, "r") as f:
            ifreq = json.loads(f.read())
            tfidf = process_tfidf(ifreq, N)
        with open("../finalWikiTfidf/" + filename, "w") as export:
            export.write(json.dumps(tfidf, indent=2))


def process_tfidf(ifreq, N):
    idfdict = {}
    for word in ifreq:
        idfdict[word] = [(doc[0], doc[1] * math.log(N / len(ifreq[word]))) for doc in ifreq[word]]
    return idfdict


def build_tfidf_norm(tfidf, doc_lengths):
    count = 0
    normtfidf = {}
    for word in tfidf:
        try:
            normtfidf[word] = [(id, freq / doc_lengths[id]) for id, freq in tfidf[word]]
        except (KeyError):
            count += 1
    print "count %s/%s" % (count, len(tfidf))
    return normtfidf


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query CACM or WIKI and get vectorial results")
    parser.add_argument("-c", "--collection", default="CACM", help="the collection to use")
    args = parser.parse_args()

    build_CACMtfidf()
