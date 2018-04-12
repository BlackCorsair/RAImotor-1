#!venv/bin/python
from pathlib import Path
from dbmanager import DBManager
from htmlparser import HTMLParser
from normalizer import Normalizer
from tabulate import tabulate
from random import randint
from collections import OrderedDict
from operator import itemgetter
import xml.etree.ElementTree
import search


class Controller:
    directory = ""
    manager = DBManager()
    parser = HTMLParser()
    normalizer = Normalizer()

    def __init__(self):
        print("Controller init")
        self.directory = "docrepository"

    def main(self):
        print('Options: 1-setup 2-run 3-exit')
        while True:
            text = input("> ")
            if(text == '1'):
                self.setup()
            elif(text == '2'):
                self.displayResults()
            elif(text == '3'):
                break
            else:
                print("Invalid input")

    def setup(self):
        print("Found the following files:")
        p = Path(self.directory)
        for i in p.iterdir():
            print("Working on file:", i.name)
            path = Path.cwd().joinpath(self.directory +
                                       "/" + i.name)
            with path.open('r') as file:
                # Parser
                filetext = self.parser.parse(file)
                # Normalizer
                normalized = self.normalizer.normalize(
                    filetext)
                # Save to DB
                if self.manager.saveDoc(i.name) == 1:
                    for term in normalized:
                        if self.manager.saveTerm(term) == 1:
                            relation = {'doc': i.name,
                                        'term': term}
                            self.manager.saveRelation(
                                relation, normalized[term])
        self.manager.updateIDF()

    def computeTable(self, topicArray, result, table, method):
        
        count = 1
        for topic in topicArray:
            index = 'Q' + str(count)
            table[index] = []
            aux = result[topic['query']]
            for r in aux:
                table['Files']= sorted(Path(self.directory).iterdir())
                if method == 1:
                    # Recuperar resultado de Producto escalar TF
                    table[index].append(r['scalarTF'])
                elif method == 2:
                    # Recuperar resultado de Producto escalar TF IDF
                    table[index].append(r['scalarTF_IDF'])
                elif method == 3:
                    # Recuperar resultado de Coseno TF
                    table[index].append(r['cosTF'])
                elif method == 4:
                    # Recuperar resultado de Coseno TF IDF
                    table[index].append(r['cosTF_IDF'])
            count = count + 1
        return table

    def displayResults(self):
        topicArray = []
        print("Running...")
        root = xml.etree.ElementTree.parse('2010-topics.xml').getroot()       
        
        for topic in root.findall('topic'):
            topicArray.append({'id':topic.get('id'),'query': topic.find('title').text})
        
        print(topicArray)
        table = OrderedDict()
        table['Files'] = []

        result = OrderedDict()

        # Compute all calculations
        for topic in topicArray:
            normalized = self.normalizer.normalize(topic['query'])
            #result[query] = sorted(search.calcAll(normalized, self.manager.docs, self.manager.relations, self.manager.terms), key=itemgetter('doc'))

        print("RELEVANCIA: CosenoTFIDF")
        table = self.computeTable(topicArray, result, table, 4)
        print(tabulate(table, headers="keys"))


controller = Controller()
controller.main()
