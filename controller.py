#!venv/bin/python
from pathlib import Path
from dbmanager import DBManager
from htmlparser import HTMLParser
from normalizer import Normalizer
from search import Search
from metrics import Metrics
from tabulate import tabulate
from collections import OrderedDict
from operator import itemgetter
import xml.etree.ElementTree
import signal
import time
import datetime
from nltk.corpus import wordnet


class Controller:
    directory = ""
    manager = DBManager()
    parser = HTMLParser()
    normalizer = Normalizer()
    searcher = Search()
    metrics = Metrics()

    def __init__(self):
        print("Controller init")
        self.directory = "docrepository"

    def main(self):
        print('Options: 1-setup 2-run 3-run_debug_mode 4-exit d-debug')
        while True:
            text = input("> ")
            if(text == '1'):
                self.setup()
            elif(text == '2'):
                self.displayResults(False)
            elif(text == '3'):
                self.displayResults(True)
            elif(text == '4'):
                break
            elif(text == 'd'):
                self.setupDebug()
            else:
                print("Invalid input")

    def setup(self):
        print("Set up init: ", datetime.datetime.now())
        print("Found the following files:")
        p = Path(self.directory)
        for i in p.iterdir():
            print("Working on file:", i.name)
            if i.name != ".gitkeep":
                path = Path.cwd().joinpath(self.directory +
                                           "/" + i.name)
                with path.open('r', encoding='ascii',
                               errors='replace') as file:
                    # Parser
                    filetext = self.parser.parse(file)
                    # Normalizer

                    def timeout_handler(num, stack):
                        raise Exception("File timeout")

                    signal.signal(signal.SIGALRM, timeout_handler)
                    signal.alarm(120)
                    try:
                        normalized = self.normalizer.normalize(filetext)
                        # Save to DB
                        if self.manager.saveDoc(i.name) == 1:
                            for term in normalized:
                                if self.manager.saveTerm(term) == 1:
                                    relation = {'doc': i.name,
                                                'term': term}
                                    self.manager.saveRelation(relation,
                                                              normalized[term])
                        self.manager.terms.reindex()
                        self.manager.docs.reindex()
                        self.manager.relations.reindex()
                    except Exception:
                        print("Unable to parse file:", i.name)
                    finally:
                        signal.alarm(0)
        self.manager.updateIDF()
        print("Set up end: ", datetime.datetime.now())

    def setupDebug(self):
        print("Found the following files:")
        p = Path(self.directory)
        number = 0
        for i in p.iterdir():
            if i.name != ".gitkeep":
                print("[" + str(number) + "] Working on file:", i.name)
                number += 1
                path = Path.cwd().joinpath(self.directory +
                                           "/" + i.name)
                try:
                    with path.open('r', encoding='ASCII',
                                   errors='replace') as file:
                        # Parser
                        start_time = time.time()
                        filetext = self.parser.parse(file)
                        print("--- %s seconds in parsing ---"
                              % (time.time() - start_time))
                        # Normalizer
                        start_time = time.time()
                        normalized = self.normalizer.normalize(filetext)
                        print("--- %s seconds in normalize ---"
                              % (time.time() - start_time))
                        # Save to DB
                        start_time = time.time()
                        if self.manager.saveDoc(i.name) == 1:
                            for term in normalized:
                                if self.manager.saveTerm(term) == 1:
                                    relation = {'doc': i.name,
                                                'term': term}
                                    self.manager.saveRelation(
                                        relation, normalized[term])
                        self.manager.terms.reindex()
                        self.manager.docs.reindex()
                        self.manager.relations.reindex()
                        print("--- %s seconds in saving ---"
                              % (time.time() - start_time))
                        print(str(len(normalized)) + ' terms saved.')
                        print(str(self.manager.terms.count()) + ' total terms.')
                except UnicodeDecodeError:
                    print('The element is not encoded in ASCII.')
        self.manager.updateIDF()

    def computeTable(self, topicArray, result, table, debug, threshold, limit):
        count = 0
        for topic in topicArray:
            index = topic['id']
            if debug:
                count = count + 1
                if count == limit:
                    break
            table[index] = []
            aux = result[topic['id']]
            for r in aux:
                # Recuperar resultado de Coseno TF IDF
                if r['cosTF_IDF'] and r['cosTF_IDF'] >= threshold:
                    table[index].append(r['doc'].split('.')[0])
        return table

    def displayResults(self, debug):
        limit = 5
        topicArray = []
        if debug:
            print("Running...")
        root = xml.etree.ElementTree.parse('2010-topics.xml').getroot()
        for topic in root.findall('topic'):
            topicArray.append({'id': topic.get('id'), 'query':
                               topic.find('title').text})
        table = OrderedDict()

        result = OrderedDict()

        # Compute all calculations
        count = 0
        for topic in topicArray:
            if debug:
                print(topic['query'])
                count = count + 1
                if count == limit:
                    break
            normalized = self.normalizer.normalize(topic['query'])
            queryArray = []
            
            for term in normalized:
                if debug:
                    print("Synonyms for term: ", term)
                ss = wordnet.synsets(term)
                if not ss:
                    queryArray.append(term)
                if not (not ss):
                    if debug:
                        print(ss[0].lemma_names())
                    for x in ss[0].lemma_names():
                        #Añadir términos relevantes a la consulta
                        queryArray.append(x)        
            if debug:
                print("Extended Query>>>>>",queryArray)
            
            result[topic['id']] = sorted(self.searcher.calcAll(queryArray, self.manager.docs, self.manager.relations, self.manager.terms), key=itemgetter('doc'))
            
        
        threshold = 0.09
        table['Metricas'] = ['numDocs','recall10', 'recall5','precision10', 'precision5','fvalue10','fvalue5', 'rrank1', 'rrank2', 'aprecision', 'nDCG10']
        table = self.computeTable(topicArray, result, table, debug, threshold, limit)
        
        count = 0
        for topic in topicArray:
            if debug:
                count = count + 1
                if count == limit:
                    break
            files = table[topic['id']]
            print(topic['id'])

            table[topic['id']] = []

            table[topic['id']].append(len(files))
            
            recall = self.metrics.cutRecall(sorted(files), topic['id'])
            table[topic['id']].append(recall['recall10'])
            table[topic['id']].append(recall['recall5'])
            
            # tests the cutPrecision
            precision = self.metrics.cutPrecision(sorted(files), topic['id'])
            table[topic['id']].append(precision['precision10'])
            table[topic['id']].append(precision['precision5'])
            
            # tests the FMeasure
            FMeasure = self.metrics.FMeasure(precision, recall)
            table[topic['id']].append(FMeasure['fvalue10'])
            table[topic['id']].append(FMeasure['fvalue5'])
            
            # tests the RRank1
            RRank1 = self.metrics.RRank1(files, topic['id'])
            table[topic['id']].append(RRank1['rrank1'])
            
            # tests the RRank2
            RRank2 = self.metrics.RRank2(files, topic['id'])
            table[topic['id']].append(RRank2['rrank2'])
            
            # tests the Aprecision
            Aprecision = self.metrics.APrecision(files, topic['id'])
            table[topic['id']].append(Aprecision['aprecision'])
            
            # tests the nDCG
            nDCG = self.metrics.nDCG(files, topic['id'], 10)
            table[topic['id']].append(nDCG['nDCG10'])
        
        '''
        table['Metricas'] = ['numDocs','recall10', 'recall5','precision10', 'precision5','fvalue10','fvalue5', 'rrank1', 'rrank2', 'aprecision', 'nDCG10']
        table['2010-001'] = [20, 0.8, 0.9,0.5833, 0.3333, 0.6363, 0.470588, 0.0769, 0.1111, 1.125, [0.5, 0.6666, 0.75, 0.6478, 0.6821, 0.6293, 0.6988, 0.69887, 0.81874]]
        table['2010-002'] = [10, 0.8, 0.6,0.5833, 0.3333, 0.6363, 0.470588, 0.0769, 0.1111, 1.125, [0.5, 0.6666, 0.75, 0.6478, 0.6821, 0.6293, 0.6988, 0.69887, 0.81874]]
        table['2010-003'] = [15, 0.8, 0.3,0.5833, 0.3333, 0.6363, 0.470588, 0.0769, 0.1111, 1.125, [0.5, 0.6666, 0.75, 0.6478, 0.6821, 0.6293, 0.6988, 0.69887, 0.81874]]
        #table['2010-004'] = [20, 0.8, 0.7,0.5833, 0.3333, 0.6363, 0.470588, 0.0769, 0.1111, 1.125, [0.5, 0.6666, 0.75, 0.6478, 0.6821, 0.6293, 0.6988, 0.69887, 0.81874]]
        #table['2010-005'] = [20, 0.8, 0.7,0.5833, 0.3333, 0.6363, 0.470588, 0.0769, 0.1111, 1.125, [0.5, 0.6666, 0.75, 0.6478, 0.6821, 0.6293, 0.6988, 0.69887, 0.81874]]
        '''
        #Calcular las medias
        avgDocs, avgR10, avgR5, avgP10, avgP5, avgF10, avgF5, avgRR1, avgRR2, avgAP = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        for topic in table:
            if topic != 'Metricas':
                avgDocs += table[topic][0]
                avgR10 += table[topic][1]
                avgR5 += table[topic][2]
                avgP10 += table[topic][3]
                avgP5 += table[topic][4]
                avgF10 += table[topic][5]
                avgF5 += table[topic][6]
                avgRR1 += table[topic][7]
                avgRR2 += table[topic][8]
                avgAP += table[topic][9]

        size = len(table) - 1
        table['Medias'] = []
        table['Medias'].append(avgDocs/size)
        table['Medias'].append(avgR10/size)
        table['Medias'].append(avgR5/size)
        table['Medias'].append(avgP10/size)
        table['Medias'].append(avgP5/size)
        table['Medias'].append(avgF10/size)
        table['Medias'].append(avgF5/size)
        table['Medias'].append(avgRR1/size)
        table['Medias'].append(avgRR2/size)
        table['Medias'].append(avgAP/size)
        print(tabulate(table, headers="keys"))

controller = Controller()
controller.main()
