#!venv/bin/python
from pymongo import MongoClient, UpdateOne, HASHED
from math import log10


class DBManager:
    client = 1
    db = 1
    docs = 1
    terms = 1
    relations = 1

    def __init__(self):
        print("DBManager: Set up Database")
        self.client = MongoClient('172.17.0.2:27017')
        self.db = self.client.db
        self.docs = self.db.docs
        self.terms = self.db.terms
        self.relations = self.db.relations
        self.terms.create_index([('term', HASHED)], name='term_index')
        self.docs.create_index([('name', HASHED)], name='doc_index')
        self.relations.create_index([('term', HASHED)], name='term_index')
        self.relations.create_index([('doc', HASHED)], name='doc_index')

    '''
        Name: saveTerm
        Input: term (string)
        Ouput: if correct execution returns '1',
               if error returns '-1'
        Function: saves the term given
    '''

    def saveTerm(self, term):
        requests = [
            UpdateOne({'term': term},
                      {'$setOnInsert': {'term': term,
                                        'idf': 0, 'ni': 0}},
                      upsert=True),
            UpdateOne({'term': term},
                      {'$inc': {'ni': 1}},
                      upsert=True)]
        try:
            self.terms.bulk_write(requests)
            return 1
        except Exception as e:
            print(e)
            return -1
    '''
        Name: saveTerms
        Input: term (string) array
        Ouput: if correct execution returns '1',
               if error returns '-1'
        Function: saves the terms given in the array
    '''

    def saveTerms(self, terms):
        for term in terms:
            self.saveTerm(term)

    '''
        Name: saveDoc
        Input: doc (string)
        Ouput: if correct execution returns 1
               if error returns '-1'
        Function: saves the doc given
    '''

    def saveDoc(self, doc):
        try:
            self.docs.update({'name': doc},
                             {'$setOnInsert': {'name': doc}}, upsert=True)
            return 1
        except Exception as e:
            print(self.docs)
            print('SaveDoc: An error ocurred:')
            print(e)
            return -1
    '''
        Name: saveRelation
        Input: relation, where relation is a dict {'doc: doc', 'term': 'term'}
              and tf, where tf is the tf of the given relation
        Ouput: if correct execution returns '1',
               if error returns '-1'
        Function: saves the relation given
    '''

    def saveRelation(self, relation, tf):
        try:
            self.relations.update({'doc': relation['doc'],
                                   'term': relation['term']},
                                  {'$set': {'tf': tf}}, upsert=True)
            return 1
        except Exception as e:
            print(e)
            return -1

    '''
        Name: getIDF
        Input: term (string)
        Output: float value containing the idf, if error returns '-1'
        Function: given a term, 'getIDF' will search in
                 the DB the term and return the IDF
    '''

    def getIDF(self, term):
        try:
            return self.terms.find_one({'term': term})['idf']
        except Exception as e:
            print(e)
            return -1

    '''
        Name: getTF
        Input: relation, where relation is a dict {'doc: doc', 'term': 'term'}
        Output: float value, if error returns '-1'
        Function: given a relation, 'getTF' will search in
                 the DB the relation and return the TF
    '''

    def getTF(self, relation):
        try:
            return self.relations.find_one({'doc': relation['doc'],
                                            'term': relation['term']})['tf']
        except Exception as e:
            print(e)
            return -1

    '''
        Name: updateIDF
        Input: none
        Output: returns 1 if correct execution,
                returns -1 if error
        Function: updates the idf value in all the terms
    '''

    def updateIDF(self):
        print("updating the idf value in all terms...")
        total_docs = self.docs.count()
        try:
            for term in self.terms.find():
                idf = log10(total_docs / term['ni'])
                self.terms.update({'term': term['term']},
                                  {'$set': {'idf': idf}},
                                  upsert=True)
        except Exception as e:
            print(e)

    '''
        Name: cleanDB
        Input: none
        Output: returns 1 if correct execution,
                returns -1 if error
        Function: removes all collections in DB
    '''

    def cleanDB(self):
        try:
            self.db.drop_collection('docs')
            self.db.drop_collection('terms')
            self.db.drop_collection('relations')
            self.db.terms.drop_indexes()
            self.db.docs.drop_indexes()
            self.db.relations.drop_indexes()
            return 1
        except Exception as e:
            print(e)
            return -1
