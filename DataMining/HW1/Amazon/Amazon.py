from Utility import *
from Classifiers import *
import numpy as np
from imblearn.over_sampling import SMOTE

Classifiers = [
	#LogisticRegression(C=3 ),
	#SVC(probability=True),
	#DecisionTreeClassifier(max_depth=6),
	#RandomForestClassifier(n_estimators=300),
	#AdaBoostClassifier(),
	#GradientBoostingClassifier(),
	#xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05)
]

def FreqVar(Data, Feature):
	Counts = Data[Feature].value_counts()
	Sum = sum(Counts.values)
	Len = len(Counts)
	if Feature == "ACTION":
		print(Counts)
	Ret = 0
	for Value in Counts:
		Ret += Value/Sum*((Value-Sum/Len)**2)
	return Ret/(10**6)

def ShowVariance(Data):
	for Feature in Data:
		"""
		if Feature == "ACTION":
			continue
		"""
		Var = FreqVar(Data, Feature)
		print("============= "+Feature+" ==============")
		print(Var)

def Preprocess(Data):
	ShowVariance(Data)
	return Data.values

def AmazonPredict():
	TrainingData = ReadTrainingData("./train.csv")
	TestingData = ReadTestingData("./test.csv")
	TestingIds = TestingData["id"].values
	

	TrainingData = Preprocess(TrainingData)
	TestingData = Preprocess(TestingData)
	
	TrainingX = TrainingData[0::, 1:9:]
	TrainingLabel = TrainingData[0::, 0]

	TestingX = TestingData[0::, 1:9:]

	#One-hot encoder
	Enc = preprocessing.OneHotEncoder()
	Enc.fit(np.vstack((TrainingX, TestingX)))
	TrainingX = Enc.transform(TrainingX)
	TestingX = Enc.transform(TestingX)
	print(TrainingX[0])
	print(TestingX[0])
	
	"""
	Smote = SMOTE()
	TrainingX, TrainingLabel = Smote.fit_sample(TrainingX, TrainingLabel)
	"""

	Spliter = StratifiedShuffleSplit(n_splits=10, test_size=0.2, random_state=0)
	
	ResultDict = {}
	for TrainIndex, TestIndex in Spliter.split(TrainingX, TrainingLabel):
		X_train, X_test = TrainingX[TrainIndex], TrainingX[TestIndex]
		y_train, y_test = TrainingLabel[TrainIndex], TrainingLabel[TestIndex]

		for clf in Classifiers:
			name = clf.__class__.__name__
			print(name)
			clf.fit(X_train, y_train)
			train_predictions = clf.predict_proba(X_test)[:, 1]
			
			#acc = accuracy_score(y_test, train_predictions)
			fpr, tpr, thresholds = roc_curve(y_test, train_predictions)
			Auc = auc(fpr, tpr)
			print("AUC = " + str(Auc))
			
			if name in ResultDict:
				ResultDict[name] += Auc
			else:
				ResultDict[name] = Auc

	for clf in ResultDict:
		ResultDict[clf] = ResultDict[clf] / 10.0
		log_entry = pd.DataFrame([[clf, ResultDict[clf]]], columns=["Classifier", "Accuracy"])
		print("===================================")
		print(log_entry)
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

AmazonPredict()
