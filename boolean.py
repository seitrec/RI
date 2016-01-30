##############################################################
# Name: Boolean
# Purpose: This modeule is designed to run boolean queries on either CACM
#          or WIKI collection
# Author: Damien Peltier & Corentin Seitre
# Created: 12/15 - 01/16
##############################################################

from parseCollection import loadJsons
import argparse


def parse_bool_query(query):
    query = query.replace("(", "").replace(")", "").replace(" ", "")
    ANDS = [[(elem[1:], "-") if elem[0] == "^" else (elem, "+") for elem in OR.split("|")] for OR in query.split("&")]
    print(ANDS)
    print("Interpreted query: %s" % (
        "(" + ") & (".join(
            " | ".join("^" + word[0] if word[1] == "-" else word[0] for word in AND) for AND in ANDS) + ")"))
    return ANDS


def find_documents(parsed_query, freq, ifreq):
    docs = set()
    init = 1
    for OR in parsed_query:
        or_docs = set()
        for condition in OR:
            print condition
            if condition[1] == "+":
                if condition[0] in ifreq:
                    or_docs = or_docs.union(set(elem[0] for elem in ifreq[condition[0]]))
            else:
                alldocs = set(freq.keys())
                NOT = alldocs if condition[0] not in ifreq else alldocs.difference(
                    set(elem[0] for elem in ifreq[condition[0]]))
                or_docs = or_docs.union(NOT)
        if init:
            docs = docs.union(or_docs)
            init = 0
        else:
            docs = docs.intersection(or_docs)
    return docs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query CACM or WIKI and get boolean results")
    parser.add_argument("-c", "--collection", default="CACM", help="The collection we want to query from")
    parser.add_argument("-q", "--query", default="(A|..|N)&(..)&..&(M|..|Z)",
                        help="The words we want to search (for several words use '' ). \
						Your query must be of the form: (A|..|N)&(..)&..&(M|..|Z) \
						and can use ^ as a specific NOT to a word. This is always possible (CNF)\
						Absolutely no space (' ') should be used")
    args = parser.parse_args()
    query = args.query
    words = query.replace("(", "").replace(")", "").replace("&", " ").replace("|", " ").replace("^", "").split(" ")
    freq, ifreq = loadJsons(args.collection, words)
    parsed_query = parse_bool_query(query)

    print find_documents(parsed_query, freq, ifreq)
