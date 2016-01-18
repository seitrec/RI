import argparse
import math

from main import *


def build_tfidf(ifreq, N):
    idfdict = {}
    for word in ifreq:
        idfdict[word] = [(doc[0], doc[1]*math.log(N/len(ifreq[word]))) for doc in ifreq[word]]
    return idfdict
        #for doc in ifreq[word]:
        #    tf = doc[1]
        #    idf = math.log(N/ifreq[word])
            


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query CACM or WIKI and get vectorial results")
    parser.add_argument("-c", "--collection", default="CACM", help="the collection to use")
    args = parser.parse_args()

    freq, ifreq = loadJsons(args.collection, {})
    if args.collection == "CACM":
        N = float(len(freq.keys()))
        tfidf = build_tfidf(ifreq, N)
        with open("../CACM/revertFreqTfidf.json", "w") as export:
            export.write(json.dumps(tfidf, indent=2))
    else:
        N = 660000
        for j, filename in enumerate(os.listdir("../finalWiki/")):
            print(j)
            with open("../finalWiki/" + filename, "r") as f:
                ifreq = json.loads(f.read())
                tfidf = build_tfidf(ifreq, N)
            with open("../finalWikiTfidf/" + filename, "w") as export:
                export.write(json.dumps(tfidf, indent=2))


