from lepl import *
def ander(result):
    if len(result) == 2:
        return (result[0], result[1])
    return result[0]
text = String() | Word()
andClausePrime = Delayed()
label = text & Drop(':')
with DroppedSpace():
    parameter = label & text > (lambda r: {r[0]: r[1]})
    andClause = (parameter | text) & andClausePrime > ander
    andClausePrime += (Drop('AND') & (andClause | parameter | text) & andClausePrime)[:]
    expr = andClause | parameter | text
    query = expr & (Drop('OR') & expr)[:]