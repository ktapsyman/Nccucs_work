from Utility import *
from Classifiers import *
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE

Classifiers = [
	#LogisticRegression(C=3 ),
	#SVC(probability=True, kernel=RbfUsingDTW),
	#KNeighborsClassifier(metric=fastdtw)
	#DecisionTreeClassifier(max_depth=6),
	#RandomForestClassifier(n_estimators=300),
	#AdaBoostClassifier(),
	#GradientBoostingClassifier(),
	#xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05)
]

def Preprocess(Data):
	return Data.values

def SignatureVerifier():
	TrainingRealSignatures = ReadDataFromDir("./dataset/Training/Real", "Real")
	TrainingFakeSignatures = ReadDataFromDir("./dataset/Training/Fake", "Fake")
	TrainingData = TrainingRealSignatures+TrainingFakeSignatures
	TrainingX = np.array([Data[1] for Data in TrainingData], dtype=object)
	TrainingLabel = np.array([Data[0] for Data in TrainingData])

	TestingRealSignatures = ReadDataFromDir("./dataset/Testing/Real", "Real")
	TestingFakeSignatures = ReadDataFromDir("./dataset/Testing/Fake", "Fake")
	TestingData = TestingRealSignatures+TestingFakeSignatures
	TestingX = np.array([Data[1] for Data in TrainingData], dtype=object)
	TestingLabel = np.array([Data[0] for Data in TrainingData])

	Spliter = StratifiedShuffleSplit(n_splits=10, test_size=0.2, random_state=0)
	
	ResultDict = {}
	for TrainIndex, TestIndex in Spliter.split(TrainingX, TrainingLabel):
		X_train, X_test = TrainingX[TrainIndex], TrainingX[TestIndex]
		y_train, y_test = TrainingLabel[TrainIndex], TrainingLabel[TestIndex]
		
		#clf.fit(X_train, y_train)
		train_predictions = KNNUsingDTW(X_train, y_train, X_test, K=6)#clf.predict_proba(X_test)[:, 1]
		
		acc = accuracy_score(y_test, train_predictions)
		if "KNN" in ResultDict:
			ResultDict["KNN"] += acc
		else:
			ResultDict["KNN"] = acc

	for clf in ResultDict:
		ResultDict[clf] = ResultDict[clf] / 10.0
		log_entry = pd.DataFrame([[clf, ResultDict[clf]]], columns=["Classifier", "Accuracy"])
		print("===================================")
		print(log_entry)
	
	RealPrediction = KNNUsingDTW(TrainingX, TrainingLabel, TestingX, K=6)
	TestingAcc = accuracy_score(RealPrediction, TestingLabel)
	print("Testing acc = " + str(TestingAcc))
	
	"""
	#Logistic
	Logistic = LogisticRegression(C=3)
	Logistic.fit(TrainingX, TrainingLabel)
	LogisticPrediction = Logistic.predict_proba(TestingX)[:, 1]
	print(len(LogisticPrediction))
	print(len(TestingIds))
	OutputData = {"id":TestingIds, "ACTION":LogisticPrediction}
	OutputDF = pd.DataFrame(data=OutputData, columns = ["id", "ACTION"])
	OutputDF.to_csv("LogisticResult.csv", index=False)
	#RF
	RFClassifier = RandomForestClassifier(n_estimators=300)
	RFClassifier.fit(TrainingX, TrainingLabel)
	RFPrediction = RFClassifier.predict_proba(TestingX)[:, 1]
	OutputData = {"id":TestingIds, "ACTION":RFPrediction}
	OutputDF = pd.DataFrame(data=OutputData, columns = ["id", "ACTION"])
	OutputDF.to_csv("RFResult.csv", index=False)
	
	#Ensemble
	Prediction = [x/2.0 for x in LogisticPrediction+RFPrediction]
	OutputData = {"id":TestingIds, "ACTION":Prediction}
	OutputDF = pd.DataFrame(data=OutputData, columns = ["id", "ACTION"])
	OutputDF.to_csv("EnsembleResult.csv", index=False)
	"""
SignatureVerifier()
