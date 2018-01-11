import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import re
import os
import xml.etree.ElementTree as ET

from Classifiers import *


Classifiers = [
	SVC(probability=False),
    DecisionTreeClassifier(),
	RandomForestClassifier(),
	AdaBoostClassifier(),
	GradientBoostingClassifier(),
	xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05)
]

FEATURE_COLUMN = [u"土地區段位置或建物區門牌", u"建物型態", u"主要建材", u"建築完成年月", u"租賃總面積平方公尺", u"建物現況格局-房", u"建物現況格局-廳", u"建物現況格局-衛", u"建物現況格局-隔間", u"有無管理組織", u"有無附傢俱", u"總額元"]
HOUSE_TYPE = [u"住宅", u"華廈", u"公寓", u"套房"]

def IsAHouse(Building):
	for Type in HOUSE_TYPE:
		if Type in Building:
			return True
	return False

def ConvertXMLToDataframe(XmlData):
	Root = ET.XML(XmlData)
	AllRecords = []
	for Record in Root:
		TransactionDetail = {}
		for TransactionColumn in Record:
			if TransactionColumn.tag not in FEATURE_COLUMN:
				continue
			TransactionDetail[TransactionColumn.tag] = TransactionColumn.text
		if not IsAHouse(TransactionDetail[u"建物型態"]):
			continue
		AllRecords.append(TransactionDetail)
	return pd.DataFrame(AllRecords)
		

def ReadTrainingData():
	PathPrefix = "./dataset/"
	Filepath = PathPrefix+"Training/"
	
	return pd.concat(ConvertXMLToDataframe(open(Filepath+"/"+FileName).read()) for FileName in os.listdir(Filepath))

def ReadTestingData():
	PathPrefix = "./dataset/"
	Filepath = PathPrefix+"Testing/"

	return pd.concat(ConvertXMLToDataframe(open(Filepath+"/"+FileName).read()) for FileName in os.listdir(Filepath))

def PreprocessDistanceFromMRT(Data):
	#TODO
	return None

def Preprocess(Data, NullFareValue):
	
	return Data.values

if __name__ == '__main__':
	TrainingData = ReadTrainingData()
	TestingData = ReadTestingData()
	
	print(TrainingData.info)
	
	"""
	Spliter = StratifiedShuffleSplit(n_splits=10, test_size=0.1, random_state=0)
	Features = TrainingData[0::, 1::]
	Labels = TrainingData[0::, 0]
	
	ResultDict = {}
	for TrainIndex, TestIndex in Spliter.split(Features, Labels):
		X_train, X_test = Features[TrainIndex], Features[TestIndex]
		y_train, y_test = Labels[TrainIndex], Labels[TestIndex]

		for clf in Classifiers:
			name = clf.__class__.__name__
			clf.fit(X_train, y_train)
			train_predictions = clf.predict(X_test)
			acc = accuracy_score(y_test, train_predictions)
			if name in ResultDict:
				ResultDict[name] += acc
			else:
				ResultDict[name] = acc

	for clf in ResultDict:
		ResultDict[clf] = ResultDict[clf] / 10.0
		log_entry = pd.DataFrame([[clf, ResultDict[clf]]], columns=["Classifier", "Accuracy"])
		print("===================================")
		print(log_entry)
	
	GBClassifier = GradientBoostingClassifier()
	GBClassifier.fit(TrainingData[0::, 1::], TrainingData[0::, 0])
	GBPrediction = GBClassifier.predict(TestingData)

	SVClassifier = SVC(probability=True)
	SVClassifier.fit(TrainingData[0::, 1::], TrainingData[0::, 0])
	SVCPrediction = SVClassifier.predict(TestingData)

	RFClassifier = RandomForestClassifier()
	RFClassifier.fit(TrainingData[0::, 1::], TrainingData[0::, 0])
	RFPrediction = RFClassifier.predict(TestingData)

	XGBoostClassifier = xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05)
	XGBoostClassifier.fit(TrainingData[0::, 1::], TrainingData[0::, 0])
	XGBPrediction = XGBoostClassifier.predict(TestingData)
	
	DTClassifier = DecisionTreeClassifier()
	DTClassifier.fit(TrainingData[0::, 1::], TrainingData[0::, 0])
	DTPrediction = DTClassifier.predict(TestingData)

	AdaClassifier = AdaBoostClassifier()
	AdaClassifier.fit(TrainingData[0::, 1::], TrainingData[0::, 0])
	AdaPrediction = AdaClassifier.predict(TestingData)
	
	Prediction=[1 if x>=2 else 0 for x in GBPrediction+SVCPrediction+RFPrediction ]

	OutputData = {"ItemId":TestingPassengerIds, "Price":Prediction}
	OutputDF = pd.DataFrame(data=OutputData)
	OutputDF.to_csv("Result.csv", index=False)
	"""
