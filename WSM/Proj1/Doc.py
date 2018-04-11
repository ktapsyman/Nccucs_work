from Utility import *

class Doc(object):
    def __init__(self, FileName, DocWordList):
        self.FileName = FileName
        self._TF = CalcTF(DocWordList)
        self._DocVector = None
    
    def GetTFDict(self):
        return self._TF
    
    def CalcDocVector(self, IDF):
        DocVec = []
        for Word in IDF:
            if Word in self._TF:
                DocVec.append(self._TF[Word]*IDF[Word])
            else:
                DocVec.append(0.0)
        self._DocVector = np.array(DocVec)
    
    def GetDocVector(self):
        return self._DocVector

