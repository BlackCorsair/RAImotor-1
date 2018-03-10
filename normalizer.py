import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class Normalizer:
    stopWords = []
    symbols = "\'!@#$~%^&*<>()_-+={}[]/.:,;|\"`"
    def __init__(self):
        print("Normalizer init")
        nltk.download('punkt')
        nltk.download('stopwords')
        self.stopWords = set(stopwords.words('english'))

    def normalize(self, text):
        #Remove stopwords
        tokenizetext = word_tokenize(text)
        #print("Original text: ", tokenizetext)
        filteredWords = []

        for w in tokenizetext:
            if self.isNotStoppedWord(self,w):
                #print("This is not a stopword:", w)
                filteredWords.append(w)

        #print ("Normalized words",filteredWords)        
        fdist = nltk.FreqDist(filteredWords)
        #print ("Original FreqDist: ", nltk.FreqDist(tokenizetext),"; Normalizer FreqDist:",fdist)
        
        return filteredWords

    def isNotStoppedWord(self, word):
        stopWords = set(stopwords.words('english')).union(['...', '\'s','--','``']);
        #print("isNotStoppedWord: word ", word)
        if(word.lower() in stopWords):
            #print("Word ", word.lower(), " is a stoppedWord")
            return False
        elif(word in self.symbols):
            #print("Word ", word, " is a symbol")
            return False
        else:
            return True