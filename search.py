#!venv/bin/python
from math import sqrt
'''
    Name: calcAll
    Input: query, which is an array of the words from the query
           relation, which is a DBManager object which can access
            the collection relations from the DB
           docs, which is a DBManager object which can access
            the collection documents from the DB,
           terms, which is a DBManager object which can access
           the collection terms from the DB
    Output: a list of dict {'doc': docname,'cosTF': value,'scalarTF': value,
                            'cosTF_IDF': value, 'scalarTF_IDF': value}
    Function: the function runs all the calculations MUAJAJAJAJAJA
'''

class Search:
    def __init__(self):
        print("Searcher init")

    def calcAll(self, query, docs, relations, terms):
        calcs = []
        qdivCosTF = sqrt(len(query))
        qdivCos = self.calcQueryCosDiv(query, terms)
        for doc in docs.find():
            # variable initialization
            scalarTF_IDF = 0
            scalarTF = 0
            divCosTF = 0
            divCosTF_DF = 0
            # middlecalc
            values = self.calcScalarDivCos(
                query, doc['name'], relations, terms)
            scalarTF = values[0]
            divCosTF = values[1]
            scalarTF_IDF = values[2]
            divCosTF_DF = values[3]
            # final calculations
            try:
                cosTFDivisor = sqrt(divCosTF) * qdivCosTF
                cosTF_IDFDivisor = sqrt(divCosTF_DF) * sqrt(qdivCos)
                cosTF = float(scalarTF / cosTFDivisor)
                cosTF_IDF = float(scalarTF_IDF / cosTF_IDFDivisor)
            except ZeroDivisionError:
                cosTF = 0
                cosTF_IDF = 0
            # return the calculations
            calcs.append({'doc': doc['name'], 'cosTF': float(cosTF),
                          'scalarTF': scalarTF, 'cosTF_IDF': cosTF_IDF,
                          'scalarTF_IDF': scalarTF_IDF})
        return calcs


    def calcScalarDivCos(self, query, doc, relations, terms):
        # all relations where appears doc
        rel = list(relations.find({'doc': doc}))
        # variable initialization
        scalarTF = 0
        scalarTF_IDF = 0
        divCosTF = 0
        divCosTF_DF = 0

        # this equals to term_tf * q
        for r in rel:
            # cosTF
            tf = r['tf']
            divCosTF = divCosTF + tf ** 2
            divCosTF_DF = divCosTF_DF + \
                (terms.find_one({'term': r['term']})['idf'] * tf) ** 2
            if r['term'] in query:
                # cosTF
                scalarTF = scalarTF + tf
                # cosTF_IDF
                idf = terms.find_one({'term': r['term']})['idf']
                # idf ** 2 = weight (idf * tf) * query_idf
                weight = idf * tf
                scalarTF_IDF = scalarTF_IDF + weight * idf
        return [scalarTF, divCosTF, scalarTF_IDF, divCosTF_DF]


    def calcQueryCosDiv(self, query, terms):
        query_cos_div_tf_df = 0
        for q in query:
            try:
                idf = terms.find_one({'term': q})['idf']
            except Exception:
                idf = 0
            query_cos_div_tf_df = query_cos_div_tf_df + idf ** 2
        return query_cos_div_tf_df
