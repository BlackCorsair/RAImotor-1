#!venv/bin/python
import multiprocessing


class Metrics:
    trelFile = ''

    def __init__(self):
        # GLOBAL VARIABLES
        self.trelFile = '2010.union.trel'
    '''
        Cut precision 5, 10
        This metric will check how many of the
        docs are relevant
    '''
    '''
        Name: cutPrecision
        In: array with the file names of the documents returned
            ¡¡¡ SORTED BY NAME !!!
        Out: returns a string showing the cut precision
        Function: given an array of filenames, it will check the
                relevance of the files and then will return an string
                showing the cut precision 5, 10
    '''

    # auxiliar function so cutPrecision can use multiple processes
    def checkRelevance(self, file):
        trel = open(self.trelFile, 'r')
        for line in trel:
            if file in line:
                return str(file), int(line.split()[3])

    def cutPrecision(self, files):
        # checks the relevance of the Files
        pool = multiprocessing.Pool()
        relevance = [pool.map(self.checkRelevance, files)]
        # saves the precision, which is relevantFiles / retrieved
        precision5 = 0.0   # first 5 files
        precision10 = 0.0  # first 10 files
        count = 0
        for (doc, rel) in sorted(relevance[0]):
            if rel >= 1 and count < 5:
                precision5 = precision5 + 0.2
            if rel >= 1 and count < 10:
                precision10 = precision10 + 0.1
            count += 1
        precision = "{'precision5': " + str(precision5) + \
                     ", 'precision10': " + str(precision10) + "}"
        return precision
