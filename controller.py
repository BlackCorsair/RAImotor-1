from pathlib import Path
from dbmanager import DBManager
from htmlparser import HTMLParser
from normalizer import Normalizer

class Controller:
        directory = ""
        manager = DBManager
        parser = HTMLParser
        normalizer = Normalizer

        def __init__(self):
                print("Controller init")
                self.directory = "docrepository"
                manager = DBManager()
                parser = HTMLParser()
                normalizer = Normalizer()

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
                                filetext = self.parser.parse(self, file)
                                # print(filetext)
                                # Normalizer
                                normalized = self.normalizer.normalize(self.normalizer, filetext)
                                # Save to DB
                                if self.manager.saveDoc(self.manager, i.name)==1:
                                        for term in normalized:
                                                print("Term ", term, " appears ", normalized[term])
                                                if self.manager.saveTerm(self.manager, term) == 1:
                                                        print("Save relation")
                                # for term in fdist:
                                # self.manager.save(self, term)
                
                queryfile = open('queryfile.txt', 'r')
                queryArray = queryfile.read().splitlines()
                for query in queryArray:
                        normalized = self.normalizer.normalize(self.normalizer, query)

        def displayResults(self):
                print("display Results Method!")


controller = Controller()
controller.main()
