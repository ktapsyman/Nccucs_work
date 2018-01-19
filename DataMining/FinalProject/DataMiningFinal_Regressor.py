import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import re
import os
import math
import xml.etree.ElementTree as ET
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import preprocessing


from Classifiers import *


#FEATURE_COLUMN = [u"土地區段位置或建物區門牌", u"建物型態", u"主要建材", u"建築完成年月", u"建物現況格局-房", u"建物現況格局-廳", u"建物現況格局-衛", u"建物現況格局-隔間", u"有無管理組織", u"有無附傢俱", u"總額元"]
FEATURE_COLUMN = [u"鄉鎮市區", u"土地區段位置或建物區門牌", u"建築完成年月", u"單價每平方公尺", u"總額元"]
#FEATURE_COLUMN = [u"土地區段位置或建物區門牌", u"建物型態", u"主要建材", u"單價每平方公尺", u"建物現況格局-房", u"建物現況格局-廳", u"建物現況格局-衛", u"建物現況格局-隔間", u"有無管理組織", u"有無附傢俱", u"總額元"]
#FEATURE_COLUMN = [u"建築完成年月", u"總額元"]
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
					TransactionColumn.text = int(TransactionColumn.text[:3])
			elif u"總額元" == TransactionColumn.text  or u"單價每平方公尺" == TransactionColumn.text:
				TransactionColumn.text = int(TransactionColumn.text)

			TransactionDetail[TransactionColumn.tag] = TransactionColumn.text
	
		if None == TransactionDetail[u"單價每平方公尺"] or TransactionDetail[u"單價每平方公尺"] == '0':
			#print(TransactionDetail[u"土地區段位置或建物區門牌"])
			continue
		"""
		HouseType = IsAHouse(TransactionDetail[u"建物型態"])
		
		if not HouseType:# or '0' == TransactionDetail[u"建物現況格局-房"]:
			continue
		else:
			TransactionDetail[u"建物型態"] = HouseType
		"""
		AllRecords.append(TransactionDetail)
	return pd.DataFrame(AllRecords)
		

def ReadTrainingData():
	PathPrefix = "./dataset/"
	Filepath = PathPrefix+"Training/"
	RetDF = pd.concat(ConvertXMLToDataframe(open(Filepath+"/"+FileName).read()) for FileName in os.listdir(Filepath))
	
	return RetDF

def ReadTestingData():
	PathPrefix = "./dataset/"
	Filepath = PathPrefix+"Testing/"
	RetDF = pd.concat(ConvertXMLToDataframe(open(Filepath+"/"+FileName).read()) for FileName in os.listdir(Filepath))

	return RetDF

def PriceRangeAcc(GroundTruth, Prediction, Tolerance=1.0):
	TransactionCount = len(GroundTruth)
	Correct = 0
	for Index in range(TransactionCount):
		if abs(GroundTruth[Index] - Prediction[Index]) <= Tolerance:
			Correct+=1
		"""
		else:
			print("Expected : " + str(GroundTruth[Index]) + " Predicted : " + str(Prediction[Index]))
		"""
			
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
	
	Latest = Data[u"建築完成年月"].max()
	Oldest = Data[u"建築完成年月"].min()
	Data[u"建築完成年月"] = Data[u"建築完成年月"]/(Latest-Oldest)
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
	Data[u"總額元"] = Data[u"總額元"].map(lambda Price:math.log10(Price))

	Data[u"總額元"] = Data[u"總額元"].astype(float)
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
	Data["Area"] = Data[u"總額元"].astype(float)/Data[u"單價每平方公尺"].astype(float)

	Smallest = Data["Area"].min()
	Largerest = Data["Area"].max()
	Data["Area"] = Data["Area"]/(Largerest-Smallest)	
	Data["Area"] = Data["Area"].astype(float)
	#print(Data["Area"])
	return Data

def Preprocess(Data):
	Data = PreprocessBuildingAge(Data)
	#Data = PreprocessTotalPrice(Data)

	DropList = [u"土地區段位置或建物區門牌"]#, u"單價每平方公尺"]
	Data = Data.drop(DropList, axis=1) 
	#Data = PreprocessBuildingType(Data)
	#Data = PreprocessInterior(Data)
	#Data = PreprocessHasManagementUnit(Data)
	#Data = PreprocessMaterial(Data)
	Data = PreprocessArea(Data)
	#Data = PreprocessDistanceFromMRT(Data)
	
	return Data

def ShowFeatureImportance(Features, Labels):
	Forest = ExtraTreesClassifier(n_estimators=300, random_state=0)
	Forest.fit(TrainingFeatures, TrainingLabels)
	Importance = Forest.feature_importances_	
	Std = np.std([tree.feature_importances_ for tree in Forest.estimators_], axis=0)
	Indices = np.argsort(Importance)[::-1]
	
	plt.figure()
	plt.title("Feature importances")
	plt.bar(range(Features.shape[1]), Importance[Indices],
       color="r", yerr=Std[Indices], align="center")
	plt.xticks(range(Features.shape[1]), Indices)
	plt.xlim([-1, Features.shape[1]])
	plt.show()
	return None

if __name__ == '__main__':
	TrainingData = ReadTrainingData()
	TestingData = ReadTestingData()

	TrainingData = Preprocess(TrainingData)
	TestingData = Preprocess(TestingData)

	TestingFeatures = TestingData.loc[:, TestingData.columns != u"總額元"]
	TestingLabels = np.asarray(TestingData[u"總額元"], dtype=int)
	print(TestingFeatures)
	print(TestingLabels)
	
	TrainingFeatures = TrainingData.loc[:, TrainingData.columns != u"總額元"]
	TrainingLabels = np.asarray(TrainingData[u"總額元"], dtype=int)

	#Encode sectors
	Enc = preprocessing.LabelEncoder()
	print(TestingFeatures.loc[:, u"鄉鎮市區"])
	print("====================")
	TestingSectors = TestingFeatures.loc[:, u"鄉鎮市區"].values
	TrainingSectors = TrainingFeatures.loc[:, u"鄉鎮市區"].values
	Sectors = np.hstack((TestingSectors, TrainingSectors))
	print(Sectors)

	Enc.fit(Sectors)
	TrainingFeatures[u"鄉鎮市區"] = Enc.transform(TrainingFeatures[u"鄉鎮市區"].values)
	TestingFeatures[u"鄉鎮市區"] = Enc.transform(TestingFeatures[u"鄉鎮市區"].values)
	
	print(TrainingFeatures.keys())
	TrainingFeatures = TrainingFeatures.values
	TestingFeatures = TestingFeatures.values
	
	#ShowFeatureImportance(TrainingFeatures, TrainingLabels)
	"""
	Smote = SMOTE()
	TrainingFeatures, TrainingLabels = Smote.fit_sample(TrainingFeatures, TrainingLabels)
	"""
	#ShowFeatureImportance(TrainingFeatures, TrainingLabels)
	"""
	Spliter = StratifiedShuffleSplit(n_splits=10, test_size=0.1, random_state=0)

	ResultDict = {}
	for TrainIndex, TestIndex in Spliter.split(TrainingFeatures, TrainingLabels):
		X_train, X_test = TrainingFeatures[TrainIndex], TrainingFeatures[TestIndex]
		y_train, y_test = TrainingLabels[TrainIndex], TrainingLabels[TestIndex]

		for clf in Classifiers:
			name = clf.__class__.__name__
			clf.fit(X_train, y_train)
			train_predictions = clf.predict(X_test)
			acc = mean_squared_error(np.log(y_test), np.log(train_predictions))
			if name in ResultDict:
				ResultDict[name] += acc
			else:
				ResultDict[name] = acc
	"""
	X_train, X_test, y_train, y_test = train_test_split(TrainingFeatures, TrainingLabels, test_size=0.2, random_state=0)
	SVRegressor = SVR()
	SVRegressor.fit(X_train, y_train)
	Result = SVRegressor.predict(X_test)
	
	MSE = mean_squared_error(np.log(y_test), np.log(Result))
	print("CV RMSE : " + str(math.sqrt(MSE)))
	

	SVRegressor = SVR()
	SVRegressor.fit(TrainingFeatures, TrainingLabels)
	SVRPrediction = SVRegressor.predict(TestingFeatures)
	SVRAcc = mean_squared_error(np.log(TestingLabels), np.log(SVRPrediction))
	print("===================================")
	print("TEST RMSE = " + str(math.sqrt(SVRAcc)))
"""
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

	GBClassifier = GradientBoostingClassifier()
	GBClassifier.fit(TrainingFeatures, TrainingLabels)
	GBPrediction = GBClassifier.predict(TestingData)
	GBAcc = PriceRangeAcc(TestingLabels, GBPrediction, 3)
	print("===================================")
	print("GB acc = " + str(GBAcc))
"""
