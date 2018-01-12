import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import re
import os
import xml.etree.ElementTree as ET

from Classifiers import *


Classifiers = [
	SVC(probability=True),
    DecisionTreeClassifier(max_depth=6),
	RandomForestClassifier(n_estimators=300),
	#AdaBoostClassifier(),
	GradientBoostingClassifier(),
	#xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05)
]

FEATURE_COLUMN = [u"土地區段位置或建物區門牌", u"建物型態", u"主要建材", u"建築完成年月", u"建物現況格局-房", u"建物現況格局-廳", u"建物現況格局-衛", u"建物現況格局-隔間", u"有無管理組織", u"有無附傢俱", u"總額元"]
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
		AreaKeyAppeared = 0
		for TransactionColumn in Record:
			if TransactionColumn.tag not in FEATURE_COLUMN:
				continue
			if u"土地區段位置或建物區門牌" == TransactionColumn.tag:
				TransactionColumn.text = TransactionColumn.text.split(u"~")[0]+u"號"
			elif u"建築完成年月" == TransactionColumn.tag:
				if TransactionColumn.text:
					TransactionColumn.text = int(TransactionColumn.text[:3])
			elif u"租賃總面積平方公尺" == TransactionColumn.tag:
				if AreaKeyAppeared != 1:
					AreaKeyAppeared += 1
					continue

			TransactionDetail[TransactionColumn.tag] = TransactionColumn.text
		HouseType = IsAHouse(TransactionDetail[u"建物型態"])
		AreaKeyAppeared = 0
		if not HouseType or '0' == TransactionDetail[u"建物現況格局-房"]:
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

def PriceRangeAcc(GroundTruth, Prediction, Tolerance=1.0):
	TransactionCount = len(GroundTruth)
	Correct = 0
	for Index in range(TransactionCount):
		#print("Trueth : " + str(GroundTruth[Index]) + " , Prediction : " + str(Prediction[Index]))
		if abs(GroundTruth[Index] - Prediction[Index]) <= Tolerance:
			Correct+=1
	return float(Correct)/float(TransactionCount)
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
	Data[u"建築完成年月"] = Data[u"建築完成年月"].astype(int)
	return Data

def PreprocessBuildingType(Data):
	Data[u"建物型態"] = Data[u"建物型態"].map({u"住宅大樓":1, u"華廈":2, u"公寓":3, u"套房":4})
	Data[u"建物型態"] = Data[u"建物型態"].astype(int)
	return Data

def PreprocessInterior(Data):
	Data[u"建物現況格局-房"] = Data[u"建物現況格局-房"].astype(int)
	Data[u"建物現況格局-房"] = Data[u"建物現況格局-廳"].astype(int)
	Data[u"建物現況格局-衛"] = Data[u"建物現況格局-衛"].astype(int)
	Data[u"建物現況格局-隔間"] = Data[u"建物現況格局-隔間"].map({u"有":1, u"無":0})
	Data[u"建物現況格局-隔間"] = Data[u"建物現況格局-隔間"].astype(int)
	Data[u"有無附傢俱"] = Data[u"有無附傢俱"].map({u"有":1, u"無":0})
	Data[u"有無附傢俱"] = Data[u"有無附傢俱"].astype(int)
	return Data

def PreprocessTotalPrice(Data):
	Data[u"總額元"] = Data[u"總額元"].map(lambda Price:int(int(Price)/1000))

	Data.loc[(Data[u"總額元"] <= 5), u"總額元"] = 0
	Data.loc[(Data[u"總額元"] > 5) & (Data[u"總額元"] <= 6), u"總額元"] = 1
	Data.loc[(Data[u"總額元"] > 6) & (Data[u"總額元"] <= 7), u"總額元"] = 2
	Data.loc[(Data[u"總額元"] > 7) & (Data[u"總額元"] <= 8), u"總額元"] = 3
	Data.loc[(Data[u"總額元"] > 8) & (Data[u"總額元"] <= 9), u"總額元"] = 4
	Data.loc[(Data[u"總額元"] > 9) & (Data[u"總額元"] <= 10), u"總額元"] = 5
	Data.loc[(Data[u"總額元"] > 10) & (Data[u"總額元"] <= 11), u"總額元"] = 6
	Data.loc[(Data[u"總額元"] > 11) & (Data[u"總額元"] <= 12), u"總額元"] = 7
	Data.loc[(Data[u"總額元"] > 12) & (Data[u"總額元"] <= 13), u"總額元"] = 8
	Data.loc[(Data[u"總額元"] > 13) & (Data[u"總額元"] <= 14), u"總額元"] = 9
	Data.loc[(Data[u"總額元"] > 14) & (Data[u"總額元"] <= 15), u"總額元"] = 10
	Data.loc[(Data[u"總額元"] > 15) & (Data[u"總額元"] <= 16), u"總額元"] = 11
	Data.loc[(Data[u"總額元"] > 16) & (Data[u"總額元"] <= 17), u"總額元"] = 12
	Data.loc[(Data[u"總額元"] > 17) & (Data[u"總額元"] <= 18), u"總額元"] = 13
	Data.loc[(Data[u"總額元"] > 18) & (Data[u"總額元"] <= 19), u"總額元"] = 14
	Data.loc[(Data[u"總額元"] > 19) & (Data[u"總額元"] <= 20), u"總額元"] = 15
	Data.loc[(Data[u"總額元"] > 20) & (Data[u"總額元"] <= 21), u"總額元"] = 16
	Data.loc[(Data[u"總額元"] > 21) & (Data[u"總額元"] <= 22), u"總額元"] = 17
	Data.loc[(Data[u"總額元"] > 22) & (Data[u"總額元"] <= 23), u"總額元"] = 18
	Data.loc[(Data[u"總額元"] > 23) & (Data[u"總額元"] <= 24), u"總額元"] = 19
	Data.loc[(Data[u"總額元"] > 24) & (Data[u"總額元"] <= 25), u"總額元"] = 20
	Data.loc[(Data[u"總額元"] > 25) & (Data[u"總額元"] <= 26), u"總額元"] = 21
	Data.loc[(Data[u"總額元"] > 26) & (Data[u"總額元"] <= 27), u"總額元"] = 22
	Data.loc[(Data[u"總額元"] > 27) & (Data[u"總額元"] <= 28), u"總額元"] = 23
	Data.loc[(Data[u"總額元"] > 28) & (Data[u"總額元"] <= 29), u"總額元"] = 24
	Data.loc[(Data[u"總額元"] > 29) & (Data[u"總額元"] <= 30), u"總額元"] = 25
	Data.loc[(Data[u"總額元"] > 30) & (Data[u"總額元"] <= 31), u"總額元"] = 26
	Data.loc[(Data[u"總額元"] > 31) & (Data[u"總額元"] <= 32), u"總額元"] = 27
	Data.loc[(Data[u"總額元"] > 32) & (Data[u"總額元"] <= 33), u"總額元"] = 28
	Data.loc[(Data[u"總額元"] > 33) & (Data[u"總額元"] <= 34), u"總額元"] = 29
	Data.loc[(Data[u"總額元"] > 34) & (Data[u"總額元"] <= 35), u"總額元"] = 30
	Data.loc[(Data[u"總額元"] > 35) & (Data[u"總額元"] <= 36), u"總額元"] = 31
	Data.loc[(Data[u"總額元"] > 36) & (Data[u"總額元"] <= 37), u"總額元"] = 32
	Data.loc[(Data[u"總額元"] > 37) & (Data[u"總額元"] <= 38), u"總額元"] = 33
	Data.loc[(Data[u"總額元"] > 38) & (Data[u"總額元"] <= 39), u"總額元"] = 34
	Data.loc[(Data[u"總額元"] > 39) & (Data[u"總額元"] <= 40), u"總額元"] = 35
	Data.loc[(Data[u"總額元"] > 40), u"總額元"] = 36

	Data[u"總額元"] = Data[u"總額元"].astype(int)
	return Data

def PreprocessHasManagementUnit(Data):
	Data[u"有無管理組織"] = Data[u"有無管理組織"].map({u"有":1, u"無":0})
	Data[u"有無管理組織"] = Data[u"有無管理組織"].astype(int)
	return Data

def PreprocessMaterial(Data):
	Data[u"主要建材"] = Data[u"主要建材"].map({u"鋼骨鋼筋混凝土造":1, u"鋼骨混凝土造":2, u"鋼筋混凝土造":3, u"加強磚造":4, u"磚造":5, u"見其他登記事項":6, u"見使用執照":6, None:6})
	Data[u"主要建材"] = Data[u"主要建材"].astype(int)
	return Data

def PreprocessArea(Data):
	Data[u"租賃總面積平方公尺"] = Data[u"租賃總面積平方公尺"].astype(int)
	return Data

def Preprocess(Data):
	Data = PreprocessBuildingType(Data)
	Data = PreprocessInterior(Data)
	Data = PreprocessBuildingAge(Data)
	Data = PreprocessTotalPrice(Data)
	Data = PreprocessHasManagementUnit(Data)
	Data = PreprocessMaterial(Data)
	#Data = PreprocessArea(Data)
	#Data = PreprocessDistanceFromMRT(Data)
	
	DropList = [u"土地區段位置或建物區門牌"]
	Data = Data.drop(DropList, axis=1) 
	return Data

if __name__ == '__main__':
	TrainingData = ReadTrainingData()
	TestingData = ReadTestingData()
	TrainingData = Preprocess(TrainingData)
	TestingData = Preprocess(TestingData)
	
	print(TestingData.info)

	TestingFeatures = TestingData.values[0::, ::-1]
	TestingLabels = np.asarray(TestingData[u"總額元"], dtype=int)
	#TestingLabels = np.asarray(TestingData[u"總額元"], dtype="|S6")

	Spliter = StratifiedShuffleSplit(n_splits=10, test_size=0.1, random_state=0)
	TrainingFeatures = TrainingData.values[0::, ::-1]
	TrainingLabels = np.asarray(TrainingData[u"總額元"], dtype=int)
	#TrainingLabels = np.asarray(TrainingData[u"總額元"], dtype="|S6")

	ResultDict = {}
	for TrainIndex, TestIndex in Spliter.split(TrainingFeatures, TrainingLabels):
		X_train, X_test = TrainingFeatures[TrainIndex], TrainingFeatures[TestIndex]
		y_train, y_test = TrainingLabels[TrainIndex], TrainingLabels[TestIndex]

		for clf in Classifiers:
			name = clf.__class__.__name__
			clf.fit(X_train, y_train)
			train_predictions = clf.predict(X_test)
			acc = PriceRangeAcc(y_test, train_predictions, 1.0)
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
	GBClassifier.fit(TrainingFeatures, TrainingLabels)
	GBPrediction = GBClassifier.predict(TestingData)
	GBAcc = PriceRangeAcc(TestingLabels, GBPrediction, 3)
	print("===================================")
	print("GB acc = " + str(GBAcc))

	SVClassifier = SVC(probability=True)
	SVClassifier.fit(TrainingFeatures, TrainingLabels)
	SVCPrediction = SVClassifier.predict(TestingData)
	SVCAcc = PriceRangeAcc(TestingLabels, SVCPrediction, 3)
	print("===================================")
	print("SVC acc = " + str(SVCAcc))

	RFClassifier = RandomForestClassifier()
	RFClassifier.fit(TrainingFeatures, TrainingLabels)
	RFPrediction = RFClassifier.predict(TestingData)
	RFAcc = PriceRangeAcc(TestingLabels, RFPrediction, 3)
	print("===================================")
	print("RF acc = " + str(RFAcc))

	DTClassifier = DecisionTreeClassifier()
	DTClassifier.fit(TrainingFeatures, TrainingLabels)
	DTPrediction = DTClassifier.predict(TestingData)
	DTAcc = PriceRangeAcc(TestingLabels, DTPrediction, 1)
	print("===================================")
	print("DT acc = " + str(DTAcc))
