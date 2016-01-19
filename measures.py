import parseQ
from sklearn.metrics import precision_recall_curve
import numpy as np

query_results = parseQ.process("CACM")
query_relevant = parseQ.
for result in query_results[0:2]:
    pred_list = result[2]
    true_list = query_relevant[result[]]
    y_scores = []
    y_true = []
    for doc in pred_list:
        y_scores.append(doc[1])
        if doc[0] in true_list:
            y_true.append(1)
        else:
            y_true.append(0)







