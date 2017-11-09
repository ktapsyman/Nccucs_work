import numpy as np
import pandas as pd
import sklearn

def ReadTrainingData(Filepath):
	return pd.read_csv(Filepath)

def ReadTestingData(Filepath):
	return pd.read_csv(Filepath)

def Preprocess(Data):
	#TODO
	return

def GenerateOutputFile(Model):
	TestingData = ReadTestingData("./test.csv")
	

if __name__ == '__main__':
	TrainingData = ReadTrainingData("./train.csv")
	print(TrainingData.isnull().sum())
	print(TrainingData.loc[TrainingData["Survived"] == True])
	TrainingData = Preprocess(TrainingData)
	
