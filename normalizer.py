import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer


class Normalizer:
    stopWords = []
    symbols = ['\'', '!', '?', '@', '#', '$', '~',
               '%', '^', '&', '*', '<', '>', '(', ')', '_', '-', '+', '=',
               '{', '}', '[', ']', '/', '.', ':', ',', ';', '|',
               '\"', '`', '“', '”', '--', '©', '®', '¦', '..', '‘',
               '’', '\'\'']

    def __init__(self):
        print("Normalizer init")
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('stopwords')
        self.stopWords = set(stopwords.words('english'))

    def normalize(self, text):
        # Remove stopwords
        tokenizetext = word_tokenize(text)
        lem = WordNetLemmatizer()
        # print("Original text: ", tokenizetext)
        filteredWords = []

        for w in tokenizetext:
            if self.isNotStoppedWord(w):
                # print("This is not a stopword:", w)
                # Remove quotation or symbol
                if w.startswith('\''):
                    w = w.replace('\'', '')
                if w.endswith('\''):
                    w = w.replace('\'', '')
                if w.endswith('�'):
                    w = w.replace('�', '')
                if w.endswith('/'):
                    w = w.replace('/', '')
                # Remove slash and append both words
                pattern = re.compile('^[a-zA-Z]+\/[a-zA-Z]+')
                if pattern.match(w):
                    x = w.split('/')
                    filteredWords.append(x[0].lower())
                    filteredWords.append(x[1].lower())
                else:
                    filteredWords.append(lem.lemmatize(w.lower()))

        # print ("Normalized words",filteredWords)
        fdist = nltk.FreqDist(filteredWords)
        # print ("Original FreqDist: ",
        # nltk.FreqDist(tokenizetext),"; Normalizer FreqDist:",fdist)
        return fdist

    def isNotStoppedWord(self, word):
        stopWords = set(stopwords.words('english')).union(
            ['...', '\'s', '--', '``'])
        # print("isNotStoppedWord: word ", word)
        if(word.lower() in stopWords):
            # print("Word ", word.lower(), " is a stoppedWord")
            return False
        elif(word in self.symbols):
            # print("Word ", word, " is a symbol")
            return False
        else:
            return True
