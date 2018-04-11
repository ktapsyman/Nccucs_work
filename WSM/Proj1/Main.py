import os
from Doc import *

DOC_ROOT_PATH = "./documents"

def QueryLoop(Docs):
    while True:
        QueryStr = input("Please input query string, or Q to quit the program")
        if QueryStr == "Q":
            break
        

def Main():
    Docs = []
    DF = {}
    for FileName in os.listdir(DOC_ROOT_PATH):
        DocStr = LoadDoc(DOC_ROOT_PATH+"/"+FileName)
        DocWordList = TokenizeDoc(DocStr)
        DocWordList = StemWords(DocWordList)
        DocWordList = RemoveStopWords(DocWordList)
        DocObj = Doc(FileName, DocWordList)
        for Word in DocObj.GetTFDict():
            if Word in DF:
                DF[Word] += 1
            else:
                DF[Word] = 1
        Docs.append(DocObj)
    
    IDF = CalcIDF(DF, len(Docs))
    for Doc in Docs:
        Doc.CalcDocVector(IDF)
    
    QueryLoop(Docs)
