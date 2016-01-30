##############################################################
# Name: Measures
# Purpose: This module is designed to measure the performance of
#          our indexing and querying algorthms
# Author: Damien Peltier & Corentin Seitre
# Created: 12/15 - 01/16
##############################################################

from parseCollection import *
from parseQueries import *


def time_indexing_CACM():
    start_time = time.time()
    with open("../Performances/Indexing-CACM-%s.txt" % (start_time), "w") as timelogs:
        frequencies = loadCACMfreq()
        timelogs.write("Index Freq processed in %.2fs\n" % (time.time() - start_time))
        revF = loadCACMst(frequencies)
        timelogs.write("Index Inverse Freq processed in %.2fs\n" % (time.time() - start_time))
        tfidf = loadCACMtfidf(frequencies, revF)
        timelogs.write("Index TfIdf processed in %.2fs\n" % (time.time() - start_time))
        loadCACMtfidfnorm(frequencies, tfidf)
        timelogs.write("Index TfIdfNorm processed in %.2fs\n" % (time.time() - start_time))


def time_queries(collection, reverseType):
    queries = parseQueries()
    parts = {item[0].rstrip(): list(itertools.chain(*([replacePunct(line[1:])
                                                       for line in item[1:]
                                                       if line[0] == "W"])))
             for item in queries}
    start_time = time.time()
    with open("../Performances/Queries-%s-%s-%s.txt" % (collection, reverseType, start_time), "w") as timelogs:
        for index, qu in parts.iteritems():
            # print(collection, index, " ".join(qu))
            start_time = time.time()
            result = (index, qu, vectorial.main(collection, reverseType, " ".join(qu)))
            timelogs.write("Query %s processed in %.2fs\n" % (index, time.time() - start_time))


if __name__ == "__main__":
    time_indexing_CACM()
    time_queries("CACM", "standard")
    time_queries("CACM", "tfidf")
    time_queries("CACM", "tfidfnorm")
    time_queries("WIKI", "standard")
    time_queries("WIKI", "tfidf")
    time_queries("WIKI", "tfidfnorm")
