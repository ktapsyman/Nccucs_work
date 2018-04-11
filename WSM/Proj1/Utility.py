from collections import Counter

import numpy as np
import nltk
from nltk.stem.snowball import *
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')
STOP_WORDS = set(stopwords.words('english')+[',', ';', ':', '!', '.', '?'])

def LoadDoc(FilePath):
    with open(FilePath, "r") as File:
        return File.read()

def TokenizeDoc(Doc):
    return nltk.word_tokenize(Doc.lower())

def StemWords(WordList):
    Stemmer = SnowballStemmer('english')
    OrginalWordList = [Stemmer.stem(Word) for Word in WordList]
    
    return OrginalWordList

def RemoveStopWords(WordList):
    global STOP_WORDS
    return[ Word for Word in WordList if Word not in STOP_WORDS ]

def CalcTF(WordList):
    return Counter(WordList)

def CalcIDF(DFDict, DocCount):
    IDF = {}
    for Word in DFDict:
        IDF[Word] = np.log(float(DocCount)/float(DFDict[Word]))
    
    return IDF
