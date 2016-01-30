##############################################################
# Name: ParseQ
# Purpose: This modeule is designed to parse the given example queries
# Author: Damien Peltier & Corentin Seitre
# Created: 12/15 - 01/16
##############################################################

from parseCollection import replacePunct
import vectorial
import itertools
import argparse
import pprint
    


def parseQueries():
    with open("../CACM/query.text", "r") as cacm:
        collection = cacm.read()
        with open("../CACM/common_words", "r") as cw:
            files = [item.split("\n.") for item in collection.split(".I ")]
            return files


def parseResults():
    parsed_resp = {}
    with open("../CACM/qrels.text", "r") as qrels:
        resps = qrels.read()
        lines = [item.split(" ") for item in resps.split("\n") if item != ""]
    for line in lines:
        if line[0] in parsed_resp:
            parsed_resp[line[0]] += [line[1]]
        else:
            parsed_resp[line[0]] = [line[1]]
    #pprint.pprint(parsed_resp)
    return parsed_resp


def process(collection, reverseType):
    queries = parseQueries()
    parts = {item[0].rstrip(): list(itertools.chain(*([replacePunct(line[1:])
                                                       for line in item[1:]
                                                       if line[0] == "W"])))
             for item in queries}
    for index, qu in parts.iteritems():
        #print(collection, index, " ".join(qu))
        yield (index, qu, vectorial.main(collection, reverseType, " ".join(qu)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query CACM or WIKI and get vectorial results")
    parser.add_argument("-c", "--collection", default="CACM", help="The collection we want to query from")
    parser.add_argument("-i", "--inverse", default="standard", help="The type of inverse freq index to use (standard, "
                                                                    "tfidf, tfidfnorm")
    args = parser.parse_args()
    #print process(args.collection, args.inverse)
