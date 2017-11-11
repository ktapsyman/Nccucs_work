import numpy as np
import pandas as pd
import sklearn

def ShowFeature(TrainingData, FeatureName):
	print("======================%s========================" % FeatureName)
	print(TrainingData[[FeatureName, "Survived"]].groupby([FeatureName], as_index=False).mean())


def ReadTrainingData(Filepath):
	return pd.read_csv(Filepath)

def ReadTestingData(Filepath):
	return pd.read_csv(Filepath)

def Preprocess(Data):
	#TODO
	del Data["Age"]
	del Data["Cabin"]
	del Data["Embarked"]
	return

def GenerateOutputFile(Model):
	TestingData = ReadTestingData("./test.csv")
	

if __name__ == '__main__':
	TrainingData = ReadTrainingData("./train.csv")
	print(TrainingData.isnull().sum())
	for Feature in ( Feature for Feature in TrainingData.columns if Feature != "Survived" and Feature != "PassengerId" and Feature != "Ticket"):
		ShowFeature(TrainingData, Feature)

	TrainingData = Preprocess(TrainingData)

	
