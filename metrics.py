#!venv/bin/python
import multiprocessing


class Metrics:
    trelFile = ''

    def __init__(self):
        # GLOBAL VARIABLES
        self.trelFile = '2010.union.trel'
    '''
        Cut Recall 5, 10
        This metric will check how many of the
        docs are relevant
    '''
    '''
        Name: cutRecall
        In: array with the file names of the documents returned
            ¡¡¡ SORTED BY NAME !!!
        Out: returns a string showing the cut Recall
        Function: given an array of filenames, it will check the
                relevance of the files and then will return an string
                showing the cut Recall 5, 10
    '''

    # auxiliar function so cutRecall can use multiple processes
    def checkRelevance(self, file):
        trel = open(self.trelFile, 'r')
        for line in trel:
            if file in line:
                return str(file), int(line.split()[3])

    def cutRecall(self, files):
        # checks the relevance of the Files
        pool = multiprocessing.Pool()
        relevance = [pool.map(self.checkRelevance, files)]
        # saves the Recall, which is relevantFiles / retrieved
        Recall5 = 0.0   # first 5 files
        Recall10 = 0.0  # first 10 files
        count = 0
        for (doc, rel) in sorted(relevance[0]):
            if rel >= 1 and count < 5:
                Recall5 = Recall5 + 0.2
            if rel >= 1 and count < 10:
                Recall10 = Recall10 + 0.1
            count += 1
        Recall = "{'Recall5': " + str(Recall5) + \
                     ", 'Recall10': " + str(Recall10) + "}"
        return Recall
