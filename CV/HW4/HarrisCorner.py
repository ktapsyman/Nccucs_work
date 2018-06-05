import sys

import numpy as np
from scipy import ndimage
import cv2

def HarrisDetector(Img, WindowSize=3, K=0.05):
		
	Img = cv2.cvtColor(Img, cv2.COLOR_BGR2GRAY)
	CornerList = np.zeros(Img.shape)
	#Dy, Dx = np.gradient(Img)
	Dx = cv2.Sobel(Img, cv2.CV_64F, 1, 0, ksize=3)
	Dy = cv2.Sobel(Img, cv2.CV_64F, 0, 1, ksize=3)
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
			CornerList[Y, X] = Response

	return CornerList

def Main():
	Img = cv2.imread(sys.argv[1])
	if Img is None:
		print("Fail to read image")
		exit()

	cv2.imshow("OriginalImg", Img)
	
	CornerList = HarrisDetector(Img.copy())
	Img[CornerList>0.01*CornerList.max()] = [0, 0, 255]
	
	cv2.imshow("Corners", Img)
	
	cv2.waitKey()
	cv2.destroyAllWindows()

Main()
