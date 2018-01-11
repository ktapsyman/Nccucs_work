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
HOUSE_TYPE = [u"住宅大樓", u"華廈", u"公寓", u"套房"]

def IsAHouse(Building):
	for Type in HOUSE_TYPE:
		if Type in Building:
			return Type
	return False

def ConvertXMLToDataframe(XmlData):
	Root = ET.XML(XmlData)
	AllRecords = []
	for Record in Root:
		TransactionDetail = {}
		for TransactionColumn in Record:
			if TransactionColumn.tag not in FEATURE_COLUMN:
				continue
			if u"土地區段位置或建物區門牌" == TransactionColumn.tag:
				TransactionColumn.text = TransactionColumn.text.split(u"~")[0]+u"號"
			elif u"建築完成年月" == TransactionColumn.tag:
				if TransactionColumn.text:
					#print("======================")
					TransactionColumn.text = int(TransactionColumn.text[:3])
					#print(TransactionColumn.text)
					
			TransactionDetail[TransactionColumn.tag] = TransactionColumn.text
		HouseType = IsAHouse(TransactionDetail[u"建物型態"])
		if not HouseType:
			continue
		else:
			TransactionDetail[u"建物型態"] = HouseType

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

def GetNearestDistanceToMRT(Address):
	#Google Map Api TODO
	Distance = 0.0
	return Distance

def PreprocessDistanceFromMRT(Data):
	#TODO
	##Using Google API perhaps
	Data["DistanceToMRT"] = Data[u"土地區段位置或建物區門牌"].apply(GetNearestDistanceToMRT)
	return Data

def PreprocessBuildingAge(Data):
	Avg = Data[u"建築完成年月"].mean()
	Std = Data[u"建築完成年月"].std()
	NullAgeCount = Data[u"建築完成年月"].isnull().sum()

	NullAgeFillList = np.random.randint(Avg-Std, Avg+Std, size=NullAgeCount)
	Data[u"建築完成年月"][np.isnan(Data[u"建築完成年月"])] = NullAgeFillList
	Data[u"建築完成年月"].astype(int)
	return Data

def PreprocessBuildingType(Data):
	print(Data[u"建物型態"])
	Data[u"建物型態"] = Data[u"建物型態"].map({u"住宅大樓":1, u"華廈":2, u"公寓":3, u"套房":4})

	return Data

def PreprocessInterior(Data):
	Data[u"建物現況格局-房"].astype(int)
	Data[u"建物現況格局-廳"].astype(int)
	Data[u"建物現況格局-衛"].astype(int)
	Data[u"建物現況格局-隔間"] = Data[u"建物現況格局-隔間"].map({u"有":1, u"無":0})
	return Data

def PreprocessTotalPrice(Data):
	Data[u"總額元"] = Data[u"總額元"].map(lambda Price:int(int(Price)/1000))
	Data[u"總額元"].astype(int)
	return Data

def PreprocessHasManagementUnit(Data):
	Data[u"有無管理組織"] = Data[u"有無管理組織"].map({u"有":1, u"無":0})
	print(Data[u"有無管理組織"])
	return Data

def PreprocessMaterial(Data):
	Data[u"主要建材"] = Data[u"主要建材"].map({u"鋼骨鋼筋混凝土造":1, u"鋼筋混凝土造":2, u"加強磚造":3, u"磚造":4, u"見其他登記事項":5})
	return Data

def Preprocess(Data):
	Data = PreprocessBuildingType(Data)
	Data = PreprocessInterior(Data)
	Data = PreprocessBuildingAge(Data)
	Data = PreprocessTotalPrice(Data)
	Data = PreprocessHasManagementUnit(Data)
	Data = PreprocessDistanceFromMRT(Data)
	Data = PreprocessMaterial(Data)
	
	DropList = [u"土地區段位置或建物區門牌"]
	Data = Data.drop(DropList, axis=1) 
	return Data#.values

if __name__ == '__main__':
	TrainingData = ReadTrainingData()
	TestingData = ReadTestingData()
	TrainingData = Preprocess(TrainingData)
	TestingData = Preprocess(TestingData)
	
	print (TrainingData.values)

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
