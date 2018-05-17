import sys

import numpy as np
import cv2

def HarrisDetector(Img, WindowSize=3, K=0.05, Threshold=10000):
	CornerList = []
		
	Img = cv2.cvtColor(Img, cv2.COLOR_BGR2GRAY)
	Dy, Dx = np.gradient(Img)
	Ixx = Dx**2
	Ixy = Dx*Dy
	Iyy = Dy**2

	Height, Width = Img.shape
	Offset = int(WindowSize/2)
	
	for Y in range(Offset, Height-Offset):
		for X in range(Offset, Width-Offset):
			Sxx = np.sum(Ixx[Y-Offset:Y+Offset+1, X-Offset:X+Offset+1])
			Sxy = np.sum(Ixy[Y-Offset:Y+Offset+1, X-Offset:X+Offset+1])
			Syy = np.sum(Iyy[Y-Offset:Y+Offset+1, X-Offset:X+Offset+1])

			Det = Sxx*Syy-Sxy**2
			Response = Det - K*((Sxx+Syy)**2)
			if Response > Threshold:
				CornerList.append((Y, X))

	return CornerList

def DrawCorners(Img, CornerList):
	for Corner in CornerList:
		cv2.circle(Img, (Corner[1], Corner[0]), 3, (0, 0, 255), 1)
	return 

def Main():
	Img = cv2.imread(sys.argv[1])
	if Img is None:
		print("Fail to read image")
		exit()
	print(Img.shape)
	cv2.imshow("OriginalImg", Img)

	CornerList = HarrisDetector(Img.copy())
	DrawCorners(Img, CornerList)
	
	cv2.imshow("Corners", Img)
	
	cv2.waitKey()
	cv2.destroyAllWindows()

Main()
