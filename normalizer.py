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
               '’', '\'\'','�','\\']
    numbers = ['0','1','2','3','4','5','6','7','8','9']

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
            if len(w) <= 20 and len(w)>2:
                if self.isNotStoppedWord(w):
                    filteredWords.append(lem.lemmatize(w.lower()))  
                    '''
                    # Remove slash and append both words
                    pattern = re.compile('^[a-zA-Z]+\/[a-zA-Z]+')
                    if pattern.match(w):
                        x = w.split('/')
                        filteredWords.append(x[0].lower())
                        filteredWords.append(x[1].lower())
                    else:
                        filteredWords.append(lem.lemmatize(w.lower()))
                    '''
        #print ("Normalized words",filteredWords)
        fdist = nltk.FreqDist(filteredWords)
        # print ("Original FreqDist: ",
        # nltk.FreqDist(tokenizetext),"; Normalizer FreqDist:",fdist)
        return fdist

    def isNotStoppedWord(self, word):
        stopWords = set(stopwords.words('english')).union(
            ['...', '\'s', '--', '``'])
        # Remove quotation or symbol
        if word.startswith('\''):
            word = word.replace('\'', '')
        if word.endswith('\''):
            word = word.replace('\'', '')
        if word.endswith('�'):
            word = word.replace('�', '')
        if word.endswith('/'):
            word = word.replace('/', '')
        if(word.lower() in stopWords):
            return False
        else:
            for char in word:
                if char in self.symbols or char in self.numbers:
                    return False
        return True
