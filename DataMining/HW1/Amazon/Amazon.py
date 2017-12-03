from Utility import *
from Classifiers import *
import numpy as np
from imblearn.over_sampling import SMOTE

Classifiers = [
	LogisticRegression(),
	#SVC(probability=True),
	#DecisionTreeClassifier(),
	RandomForestClassifier(n_estimators=100),
	#AdaBoostClassifier(),
	GradientBoostingClassifier(),
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
	
	TrainingX = TrainingData[0::, 3::]
	TrainingLabel = TrainingData[0::, 0]

	TestingX = TestingData[0::, 3::]

	#One-hot encoder
	Enc = preprocessing.OneHotEncoder()
	Enc.fit(np.vstack((TrainingX, TestingX)))
	TrainingX = Enc.transform(TrainingX)
	TestingX = Enc.transform(TestingX)
	
	Smote = SMOTE()
	TrainingX, TrainingLabel = Smote.fit_sample(TrainingX, TrainingLabel)

	Spliter = StratifiedShuffleSplit(n_splits=10, test_size=0.1, random_state=0)
	Features = TrainingData[0::, 3::]
	Labels = TrainingData[0::, 0]
	
	ResultDict = {}
	for TrainIndex, TestIndex in Spliter.split(Features, Labels):
		X_train, X_test = Features[TrainIndex], Features[TestIndex]
		y_train, y_test = Labels[TrainIndex], Labels[TestIndex]

		for clf in Classifiers:
			name = clf.__class__.__name__
			print(name)
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
	Logistic = LogisticRegression()
	Logistic.fit(TrainingX, TrainingLabel)
	Prediction = Logistic.predict(TestingX)
	
	OutputData = {"id":TestingIds, "ACTION":Prediction}
	OutputDF = pd.DataFrame(data=OutputData, columns = ["id", "ACTION"])
	OutputDF.to_csv("Result.csv", index=False)

AmazonPredict()
