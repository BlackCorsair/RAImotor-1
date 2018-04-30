#!venv/bin/python
import multiprocessing


class Metrics:
    trelFile = ''

    def __init__(self):
        # GLOBAL VARIABLES
        self.trelFile = '2010.union.trel'
    '''
        Cut precission 5, 10
        This metric will check how many of the
        docs are relevant
    '''
    '''
        Name: cutPrecission
        In: array with the file names of the documents returned
            ¡¡¡ SORTED BY NAME !!!
        Out: returns a string showing the cut precission
        Function: given an array of filenames, it will check the
                relevance of the files and then will return an string
                showing the cut precission 5, 10
    '''

    # auxiliar function so cutPrecission can use multiple processes
    def checkRelevance(self, file):
        trel = open(self.trelFile, 'r')
        for line in trel:
            if file in line:
                return str(file), int(line.split()[3])

    def cutPrecission(self, files):
        # checks the relevance of the Files
        pool = multiprocessing.Pool()
        relevance = [pool.map(self.checkRelevance, files)]
        # saves the precision, which is relevantFiles / retrieved
        precission5 = 0.0   # first 5 files
        precission10 = 0.0  # first 10 files
        count = 0
        for (doc, rel) in relevance[0]:
            if rel >= 1 and count < 5:
                precission5 = precission5 + 0.2
            if rel >= 1 and count < 10:
                precission10 = precission10 + 0.1
            count += 1
        precission = "{'precission5': " + str(precission5) + \
                     ", 'precission10': " + str(precission10) + "}"
        return precission

        # testing
        '''
        for (doc, rel) in relevance[0]:
            print(doc + ", " + str(rel))
        print(precission5)
        print(precission10)
        '''
