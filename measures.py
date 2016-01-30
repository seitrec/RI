##############################################################
# Name: Measures
# Purpose: This modeule is designed to measure the performance and results
#          of our algorithms
# Author: Damien Peltier & Corentin Seitre
# Created: 12/15 - 01/16
##############################################################

import parseQ
import json
import pprint
from sklearn.metrics import precision_recall_curve

query_results = parseQ.process("CACM")
query_relevant = parseQ.parseResp()

y_scores = []
y_true = []

for result in query_results:
    if result[0] in query_relevant.keys():
        pred_list = result[2]
        true_list = query_relevant[result[0]]
        for doc in pred_list:
            y_scores.append(doc[1])
            if doc[0] in true_list:
                y_true.append(1)
            else:
                y_true.append(0)

print(len(y_true))
print(len(y_scores))













