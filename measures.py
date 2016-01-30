##############################################################
# Name: Measures
# Purpose: This module is designed to measure the performance and results
#          of our algorithms
# Author: Damien Peltier & Corentin Seitre
# Created: 12/15 - 01/16
##############################################################

import parseQueries
import argparse
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score



def compute_results(query_results, query_relevant):
    y_scores = []  # list of scores from the search engine for each (query, document) couple
    y_true = []  # 1 if the document is relevant for the query 0 otherwise
    nb_queries = 0
    for result in query_results:
        if result[0] in query_relevant.keys():
            nb_queries += 1
            y_scores_temp = []
            y_true_temp = []
            pred_list = result[2]
            true_list = query_relevant[result[0]]
            for doc in pred_list:
                y_scores.append(doc[1])
                y_scores_temp.append(doc[1])
                if doc[0] in true_list:
                    y_true.append(1)
                    y_true_temp.append(1)
                else:
                    y_true.append(0)
                    y_true_temp.append(0)
            # We print the AP score for each single query
            print(result[0], average_precision_score(y_true_temp,y_scores_temp))

    precision, recall, thresholds = precision_recall_curve(y_true, y_scores)
    AP = average_precision_score(y_true, y_scores)
    return nb_queries, precision, recall, AP

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Measures results of our vectorial algo on a test batch")
    parser.add_argument("-c", "--collection", default="CACM", help="The collection we want to query from")
    parser.add_argument("-i", "--inverse", default="tfidf", help="Measure used for the test (standard, tfidf, tfidfnorm")
    args = parser.parse_args()
    query_results = parseQueries.process(args.collection, args.inverse) #results from our search engine
    query_relevant = parseQueries.parseResults() #relevant document for each queries
    nb_queries, precision, recall, AP = compute_results(query_results, query_relevant)
    #Printing the Precision - Recall Curve
    plt.clf()
    plt.plot(recall, precision, label='Precision-Recall curve (AP score %0.2f)' % AP)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title('Precision-Recall Curve for %i queries' % nb_queries)
    plt.legend(loc="upper right")
    plt.show()










