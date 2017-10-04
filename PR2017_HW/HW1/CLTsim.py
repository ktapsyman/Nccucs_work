import numpy as np
import matplotlib.pyplot as plot
import sys, getopt
from enum import Enum

class Distribution(Enum):
	UNIFORM = 1
	CHISQUARE = 2
	POISSON = 3
	

def GenerateRandom( Type=Distribution.UNIFORM, Size=1000, Lamda=0.5 ):
	RetDistArr = np.zeros(1000)
	if Type == Distribution.UNIFORM:
		for iter in range(0, Size):
			RetDistArr = np.array(RetDistArr + np.random.uniform(0.0, 1.0, 1000))
	elif Type == Distribution.CHISQUARE:
		for iter in range(0, Size):
			RetDistArr = np.array(RetDistArr + np.random.chisquare(2, 1000))
	elif Type == Distribution.POISSON:
		for iter in range(0, Size):
			RetDistArr = np.array(RetDistArr + np.random.poisson(Lamda, 1000))
	return RetDistArr

def GetDistributionFromArgv():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hd:")
	except getopt.GetoptError:
		print("Usage : -h for help, -d[UNIFORM or POISSON]")
		sys.exit()

	if None == opts or 0 == len(opts):
		print("Usage : -h for help, -d[UNIFORM or POISSON]")
		sys.exit()

	for opt, arg in opts:
		if opt == "-h":
			print("Usage : -h for help, -d[UNIFORM or POISSON]")
			sys.exit()
		elif opt == "-d":
			if arg == "UNIFORM":
				return Distribution.UNIFORM
			elif arg == "CHI":
				return Distribution.CHISQUARE
			elif arg == "POISSON":
				return Distribution.POISSON
			else:
				print("Invalid distribution. Using UNIFORM")
				return Distribution.UNIFORM


RandomArr = []
Dist = GetDistributionFromArgv()

for iter in range(0, 6):
	RandomArr.append(np.array(GenerateRandom(Type=Dist, Size = 10**(iter))))
iter = 0
for Arr in RandomArr:
	count, bins, ignored = plot.hist(Arr, 50, normed=True)
	plot.title("N = " + str(10**iter))
	iter+=1
	plot.show()
