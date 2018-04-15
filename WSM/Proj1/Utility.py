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
	IDF = []
	for Word in DFDict:
		IDF.append(np.log(float(DocCount)/float(DFDict[Word])))
	
	return np.array(IDF)

def EuclideanDistance(Vector1, Vector2):
	return np.linalg.norm(Vector2-Vector1)

def CosineSimilarity(Vector1, Vector2):
	return np.inner(Vector1, Vector2)/(np.linalg.norm(Vector1)*np.linalg.norm(Vector2))

def Normalized(Vector):
	return Vector/np.linalg.norm(Vector)

