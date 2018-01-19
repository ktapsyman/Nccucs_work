import os
import csv

import numpy as np
from fastdtw import fastdtw

"""
class Signature(object):
	def __init__(self, label, penPoints):
		self.label = label
		self.penPoints = penPoints
	

class PenPoint(object):
	def __init__(self, xPos, yPos, pressure, timestamp):
		self.X = xPos
		self.Y = yPos
		self.pressure = pressure
		self.timestamp = timestamp
"""

def ReadDataFromDir(DirPath, Label):
	FileList = [SignatureRawData for SignatureRawData in os.listdir(DirPath) if "txt" in SignatureRawData]
	SignatureList = []
	
	MinXY = float("inf")
	MaxXY = 0
	
	MinTimeDiff = 0 # must be 0
	MaxTimeDiff = 0
	
	for FileName in FileList:
		with open(DirPath + "/"+FileName, 'r') as SignatureFile:
			PenPointReader = csv.reader(SignatureFile, delimiter=',')
			PenPoints = []
			FirstRow = True
			PrevTimeStamp = 0
			for Row in PenPointReader:
				if FirstRow:
					PenPoints.append(np.array([Row[0], Row[1], Row[2], 0], dtype=float))
					FirstRow = False
				else:
					TimeDiff = int(Row[3])-PrevTimeStamp
					if TimeDiff > MaxTimeDiff:
						MaxTimeDiff = TimeDiff
					MinXY = min(MinXY, float(Row[0]), float(Row[1]))
					MaxXY = max(MaxXY, float(Row[0]), float(Row[1]))
					PenPoints.append(np.array([Row[0], Row[1], Row[2], TimeDiff], dtype=float))
				PrevTimeStamp = int(Row[3])
		if Label == "Real":
			SignatureList.append([1, np.array(PenPoints)])
		else:
			SignatureList.append([0, np.array(PenPoints)])
	DivVector = np.array([MaxXY-MinXY, MaxXY-MinXY, 1.0, MaxTimeDiff-MinTimeDiff])
	for SignatureData in SignatureList:
		SignatureData[1] /= DivVector
	return SignatureList

def KNNUsingDTW(TrainingSet, TrainingLabel, TestingSet, K=5):
	if K <= 0:
		print("K should be greater than 0!")
		return
	elif K >= len(TrainingSet):
		print("K should be less than len(TrainingSet)!")
		return

	Prediction = []
	for TestingData in TestingSet:
		DTWList = [(fastdtw(TestingData, TrainingSet[Index])[0], TrainingLabel[Index]) for Index in range(len(TrainingSet))]
		DTWList.sort(key=lambda x : x[0])
		DTWList = [DtwTuple[1] for DtwTuple in DTWList[:K]]
		Label = max(set(DTWList), key=DTWList.count)
		Prediction.append(Label)
		
	return Prediction

def ExtractLNPSDescriptor(Signature):
	#TODO
	return None

def RbfUsingDTW(Vector1, Vector2, Gamma):
	DtwDistance, DtwPath = fastdtw(Vector1, Vector2)
	return np.exp(-Gamma*DtwDistance**2)
