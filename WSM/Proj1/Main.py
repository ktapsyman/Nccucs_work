import os
from Doc import *

DOC_ROOT_PATH = "./documents"

def Preprocessing(DocStr):
	DocWordList = TokenizeDoc(DocStr)
	DocWordList = StemWords(DocWordList)
	DocWordList = RemoveStopWords(DocWordList)

	return DocWordList
	

def QueryLoop(Docs, BagOfWords, WordCategory, IDF):
	while True:
		QueryStr = input("Please input query string, or Q to quit the program\n")
		if QueryStr == "Q":
			break
		QueryWordList = Preprocessing(QueryStr)
		QueryDoc = Doc("", QueryWordList)
		QueryDoc.CalcDocVector(BagOfWords, WordCategory, IDF)
		
		ResultDict = {"TF-Cosine":[], "TF-Euclidean":[], "TFIDF-Cosine":[], "TFIDF-Euclidean":[]}
		for Document in Docs:
			SimilarityDict = CalcSimilarityOfTwoDocs(Document, QueryDoc)
			ResultDict["TF-Cosine"].append((Document, SimilarityDict["TF-Cosine"]))
			ResultDict["TF-Euclidean"].append((Document, SimilarityDict["TF-Euclidean"]))
			ResultDict["TFIDF-Cosine"].append((Document, SimilarityDict["TFIDF-Cosine"]))
			ResultDict["TFIDF-Euclidean"].append((Document, SimilarityDict["TFIDF-Euclidean"]))

		for Metric in ResultDict:
			ResultDict[Metric] = sorted(ResultDict[Metric], key=lambda x:x[1], reverse=("Euclidean" not in Metric))[:5]
			print(Metric)
			for Result in ResultDict[Metric]:
				print((Result[0].Id, Result[1]))
			print("===========================")
		
		ResultDict["TFIDF-RF-Cosine"] = []
		PseudoFeedBack = ResultDict["TFIDF-Cosine"][0][0]
		RFQueryVector = QueryDoc.GetDocVector("TF-IDF") + 0.5*PseudoFeedBack.GetDocVector("TF-IDF-NV-ONLY")
		for Document in Docs:
			ResultDict["TFIDF-RF-Cosine"].append((Document, CosineSimilarity(Document.GetDocVector("TF-IDF"), RFQueryVector)))
		ResultDict["TFIDF-RF-Cosine"] = sorted(ResultDict["TFIDF-RF-Cosine"], key=lambda x:x[1], reverse=True)[:5]
		print("TFIDF-RF-Cosine")
		for Result in ResultDict["TFIDF-RF-Cosine"]:
			print((Result[0].Id, Result[1]))

def Main():
	Docs = []
	DF = {}
	for FileName in os.listdir(DOC_ROOT_PATH):
		DocStr = LoadDoc(DOC_ROOT_PATH+"/"+FileName)
		DocWordList = Preprocessing(DocStr)
		DocObj = Doc(FileName, DocWordList)
		for Word in DocObj.GetTFDict():
			if Word in DF:
				DF[Word] += 1
			else:
				DF[Word] = 1
		Docs.append(DocObj)
	
	BagOfWords = np.array(list(DF.keys()))
	WordCategory = GetWordCategory(list(DF.keys()))
	IDF = CalcIDF(DF, len(Docs))
	for Document in Docs:
		Document.CalcDocVector(BagOfWords, WordCategory, IDF)
	QueryLoop(Docs, BagOfWords, WordCategory, IDF)

Main()
