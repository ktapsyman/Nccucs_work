import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import re

from Classifiers import *

Classifiers = [
#    KNeighborsClassifier(3),
	SVC(probability=True),
#    DecisionTreeClassifier(),
	RandomForestClassifier(),
	AdaBoostClassifier(),
	GradientBoostingClassifier(),
#    GaussianNB(),
#    LinearDiscriminantAnalysis(),
#    QuadraticDiscriminantAnalysis(),
#    LogisticRegression()
]

def ShowFeature(TrainingData, FeatureName):
	print("======================%s========================" % FeatureName)
	print(TrainingData[[FeatureName, "Survived"]].groupby([FeatureName], as_index=False).mean())

def ReadTrainingData(Filepath):
	return pd.read_csv(Filepath)

def ReadTestingData(Filepath):
	return pd.read_csv(Filepath)

def ExtractTitleFromName(Name):
	RegexResult = re.search(" ([A-Za-z]+)\.", Name)
	if RegexResult:
		return RegexResult.group(1)
	return ""

def ProcessName(Data):
	Data["Title"] = Data["Name"].apply(ExtractTitleFromName)

	Data["Title"] = Data["Title"].replace(["Capt", "Col", "Dr", "Jonkheer", "Major", "Rev"], "Rare")
	Data["Title"] = Data["Title"].replace(["Don", "Jonkheer", "Rev"], "Mr")
	Data["Title"] = Data["Title"].replace(["Ms", "Mlle", "Lady", "Countess"], "Miss")
	Data["Title"] = Data["Title"].replace(["Mme"], "Mrs")
	
	"""
	0  Master  0.575000
	1    Miss  0.705882
	2      Mr  0.156371
	3     Mrs  0.793651
	4    Rare  0.263158
	5     Sir  1.000000

	"""
	Data["Title"] = Data["Title"].map({"Master":1, "Miss":2, "Mr":3, "Mrs":4, "Rare":5, "Sir":6})
	Data["Title"] = Data["Title"].fillna(0)
	return Data

def ProcessSex(Data):
	Data["Sex"] = Data["Sex"].map({"male":0, "female":1}).astype(int)
	return Data

def ProcessFare(Data):
	Data["Fare"] = Data["Fare"].fillna(Data["Fare"].median())
	Data.loc[(Data["Fare"] <= 15.0), "Fare"] = 0
	Data.loc[(Data["Fare"] > 15.0) & (Data["Fare"] <= 70.0), "Fare"] = 1
	Data.loc[(Data["Fare"] > 70.0), "Fare"] = 2
	Data["Fare"] = Data["Fare"].astype(int)
	return Data

def ProcessCompanions(Data):
	Data["IsAlone"] = 0
	Data.loc[Data["SibSp"]+Data["Parch"] == 0, "IsAlone"] = 1
	Data["IsAlone"].astype(int)
	return Data

def ProcessAge(Data):
	Avg = Data["Age"].mean()
	Std = Data["Age"].std()
	NullAgeCount = Data["Age"].isnull().sum()

	NullAgeFillList = np.random.randint(Avg-Std, Avg+Std, size=NullAgeCount)
	Data["Age"][np.isnan(Data["Age"])] = NullAgeFillList
	Data["Age"] = Data["Age"].astype(int)
	
	Data.loc[Data["Age"] <= 10, "Age"] = 0
	Data.loc[(Data["Age"] > 10) & (Data["Age"] <= 20), "Age"] = 1
	Data.loc[(Data["Age"] > 20) & (Data["Age"] <= 30), "Age"] = 2
	Data.loc[(Data["Age"] > 30) & (Data["Age"] <= 40), "Age"] = 3
	Data.loc[(Data["Age"] > 40) & (Data["Age"] <= 50), "Age"] = 4
	Data.loc[(Data["Age"] > 50) & (Data["Age"] <= 60), "Age"] = 5
	Data.loc[(Data["Age"] > 60) & (Data["Age"] <= 70), "Age"] = 5
	Data.loc[(Data["Age"] > 70) & (Data["Age"] <= 80), "Age"] = 7
	Data.loc[(Data["Age"] > 80), "Age"] = 8
	return Data

def ProcessCabin(Data):
	Data = Data.assign(CabinsClass=pd.Series([str(cabin)[0] for cabin in Data["Cabin"]]).values)
	Data["CabinsClass"] = Data["CabinsClass"].map(lambda cabin:ord(cabin)-ord('A')).astype(int)
	return Data

def ProcessEmbarked(Data):
	Data["Embarked"] = Data["Embarked"].fillna("S").map({"C":0, "Q":1, "S":2}).astype(int)
	return Data

def Preprocess(Data):
	Data = ProcessName(Data)
	Data = ProcessSex(Data)
	Data = ProcessCabin(Data)
	Data = ProcessFare(Data)
	Data = ProcessEmbarked(Data)
	Data = ProcessAge(Data)
	Data = ProcessCompanions(Data)
	"""
	PassengerId    891 non-null int64
	Survived       891 non-null int64
	Pclass         891 non-null int64
	Name           891 non-null object
	Sex            891 non-null object
	Age            714 non-null float64
	SibSp          891 non-null int64
	Parch          891 non-null int64
	Ticket         891 non-null object
	Fare           891 non-null float64
	Cabin          204 non-null object
	Embarked       889 non-null object
	"""
	DropList = ["PassengerId", "Name", "SibSp", "Parch", "Ticket", "Cabin"]
	Data = Data.drop(DropList, axis=1)
	return Data.values

def GenerateOutputFile(Model):
	return
	

if __name__ == '__main__':
	TrainingData = ReadTrainingData("./train.csv")
	TestingData = ReadTestingData("./test.csv")
	TestingPassengerIds = TestingData["PassengerId"].values
	
	TrainingData = Preprocess(TrainingData)
	TestingData = Preprocess(TestingData)
	
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
	
	BestWorkingClassifier = GradientBoostingClassifier()
	BestWorkingClassifier.fit(TrainingData[0::, 1::], TrainingData[0::, 0])
	Prediction = BestWorkingClassifier.predict(TestingData)

	print(Prediction)
	OutputData = {"PassengerId":TestingPassengerIds, "Survived":Prediction}
	OutputDF = pd.DataFrame(data=OutputData)
	OutputDF.to_csv("Result.csv", index=False)
