from Utility import *

class Doc(object):
	def __init__(self, FileName, DocWordList):
		if FileName is None or len(FileName) == 0:
			self.Id = "Query"
		else:
			self.Id = FileName.split(".")[0]
		self._RawTF = CalcTF(DocWordList)
		self._DocVector = {"TF":[], "TD-IDF":[]}
	
	def GetTFDict(self):
		return self._RawTF
	
	def CalcDocVector(self, BagOfWords, IDFVec):
		for Word in BagOfWords:
			if Word in self._RawTF:
				self._DocVector["TF"].append(self._RawTF[Word])
			else:
				self._DocVector["TF"].append(0.0)
		
		self._DocVector["TF"] = np.array(self._DocVector["TF"]) #Normalized(np.array(self._DocVector["TF"]))
		self._DocVector["TF-IDF"] = self._DocVector["TF"]*IDFVec

	def GetDocVector(self, Mode=""):
		if Mode is None or 0 == len(Mode):
			return self._DocVector
		elif Mode not in self._DocVector:
			print("Invelid parameter")
			return None
		
		return self._DocVector[Mode]


def CalcSimilarityOfTwoDocs(Doc1, Doc2):
	Doc1VectorDict = Doc1.GetDocVector()
	Doc2VectorDict = Doc2.GetDocVector()
	ResultDict = {"TF-Cosine":0.0, "TF-Euclidean":0.0, "TFIDF-Cosine":0.0, "TDIDF-Euclidean":0.0}

	ResultDict["TF-Cosine"] = CosineSimilarity(Doc1VectorDict["TF"], Doc2VectorDict["TF"])
	ResultDict["TF-Euclidean"] = EuclideanDistance(Doc1VectorDict["TF"], Doc2VectorDict["TF"])
	ResultDict["TFIDF-Cosine"] = CosineSimilarity(Doc1VectorDict["TF-IDF"], Doc2VectorDict["TF-IDF"])
	ResultDict["TFIDF-Euclidean"] = EuclideanDistance(Doc1VectorDict["TF-IDF"], Doc2VectorDict["TF-IDF"])
	
	return ResultDict

