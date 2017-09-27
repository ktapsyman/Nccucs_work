import numpy as np
import matplotlib.pyplot as plot
import sys
from enum import Enum

class Distribution(Enum):
	UNIFORM = 1
	POISSON = 3
	

def GenerateRandom( Type=Distribution.UNIFORM, Size=1000, Lamda=1.0, Mean = 0.0, StdDev=1.0 ):
	RetDistArr = np.zeros(1000)
	if Type == Distribution.UNIFORM:
		for iter in range(0, Size):
			RetDistArr = np.array(RetDistArr + np.random.uniform(0.0, 1.0, 1000))
	elif Type == Distribution.POISSON:
		for iter in range(0, Size):
			RetDistArr = np.array(RetDistArr + np.random.poisson(Lamda, 1000))
	return RetDistArr


RandomArr = []
for iter in range(0, 6):
	RandomArr.append(np.array(GenerateRandom(Size = 10**(iter))))
iter = 0
for Arr in RandomArr:
	count, bins, ignored = plot.hist(Arr, 50, normed=True)
	plot.title("N = " + str(10**iter))
	iter+=1
	plot.show()
