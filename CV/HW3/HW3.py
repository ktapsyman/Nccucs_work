import cv2
import numpy as np
from matplotlib import pyplot as plt

import sys
import operator

def CalculateCDFFrom2DPixels(Pixels):
	CurrentCumulativeValue = 0
	CDF = {}
	PixelIntensityDict = {}
	Height, Width = Pixels.shape

	for Row in range(0, Height):
		for Col in range(0, Width):
			if Pixels[Row][Col] in PixelIntensityDict:
				PixelIntensityDict[Pixels[Row][Col]] += 1
			else:
				PixelIntensityDict[Pixels[Row][Col]] = 1
	
	PixelIntensityDict = dict(sorted(PixelIntensityDict.items(), key=operator.itemgetter(0)))
	for Pixel in PixelIntensityDict:
		CurrentCumulativeValue += PixelIntensityDict[Pixel]
		CDF[Pixel] = CurrentCumulativeValue

	return CDF

def CreateHistogramEqualizer(CDFMin, ImgSize, GrayScaleLevel=256):
	HistogramEqualizer = lambda CDFofPixel: round((CDFofPixel-CDFMin)*(GrayScaleLevel-1)/(ImgSize-1.0))

	return HistogramEqualizer

def HistogramEqualize(Img):
	CDF = CalculateCDFFrom2DPixels(Img)
	CDFMin = list(CDF)[0]
	HistogramEqualizer = CreateHistogramEqualizer(CDFMin, Img.size)

	Height, Width = Img.shape
	for Row in range(0, Height):
		for Col in range(0, Width):
			Img[Row][Col] = HistogramEqualizer(CDF[Img[Row][Col]])

	return Img

def ShowComparison(Title, ImgTuple):
	if Title is None or 0 == len(Title):
		Title = "Default Title"
	
	ComparisonImg = np.hstack(ImgTuple)
	cv2.imshow(Title, ComparisonImg)

def ShowImgHist(Img):
	Colors = ["b", "g", "r"]
	for Index, Color in enumerate(Colors):
		Hist = cv2.calcHist([Img], [Index], None, [256], [0, 256])
		plt.plot(Hist, color=Color)
		plt.xlim([0, 256])
	plt.show()

def Q1():
	Img = cv2.imread("hw3.jpg", cv2.IMREAD_GRAYSCALE)
	EqualizedImg = HistogramEqualize(Img.copy())
	OpenCVEqImg = cv2.equalizeHist(Img.copy())
	ShowComparison("Q1", (Img, EqualizedImg, OpenCVEqImg, EqualizedImg-OpenCVEqImg))
	return

def Q2():
	Img = cv2.imread("hw3a.jpg", cv2.IMREAD_COLOR)
	Q2a(Img.copy())
	Q2b(Img.copy())
	Q2c(Img.copy())

	return

def Q2a(Img):
	ShowImgHist(Img)
	BChannel, GChannel, RChannel = cv2.split(Img)

	# B
	EqualizedBChannel = HistogramEqualize(BChannel.copy())
	OpenCVEqualizedBChannel = cv2.equalizeHist(BChannel.copy())

	# G
	EqualizedGChannel = HistogramEqualize(GChannel.copy())
	OpenCVEqualizedGChannel = cv2.equalizeHist(GChannel.copy())

	# R
	EqualizedRChannel = HistogramEqualize(RChannel.copy())
	OpenCVEqualizedRChannel = cv2.equalizeHist(RChannel.copy())
	
	EqualizedImg = cv2.merge((EqualizedBChannel, EqualizedGChannel, EqualizedRChannel))
	ShowImgHist(EqualizedImg)
	OpenCVEqImg = cv2.merge((OpenCVEqualizedBChannel, OpenCVEqualizedGChannel, OpenCVEqualizedRChannel))
	ShowComparison("Q2a", (Img, EqualizedImg, OpenCVEqImg, EqualizedImg-OpenCVEqImg))
	return

def Q2b(Img):
	Img = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)
	HChannel, SChannel, VChannel = cv2.split(Img)

	EqulizedVChannel = HistogramEqualize(VChannel.copy())
	OpenCVEqulizedVChannel = cv2.equalizeHist(VChannel.copy())

	EqualizedImg = cv2.merge((HChannel, SChannel, EqulizedVChannel))
	OpenCVEqImg = cv2.merge((HChannel, SChannel, OpenCVEqulizedVChannel))
	ShowComparison("Q2b", (Img, EqualizedImg, OpenCVEqImg, EqualizedImg-OpenCVEqImg))

	return

def Q2c(Img):
	Img = cv2.cvtColor(Img, cv2.COLOR_BGR2YCR_CB)
	YChannel, CbChannel, CrChannel = cv2.split(Img)

	EqulizedYChannel = HistogramEqualize(YChannel.copy())
	OpenCVEqulizedYChannel = cv2.equalizeHist(YChannel.copy())

	EqualizedImg = cv2.merge((EqulizedYChannel, CbChannel, CrChannel))
	OpenCVEqImg = cv2.merge((OpenCVEqulizedYChannel, CbChannel, CrChannel))
	ShowComparison("Q2c", (Img, EqualizedImg, OpenCVEqImg, EqualizedImg-OpenCVEqImg))
	return

def Main():
	Q1()
	Q2()
	cv2.waitKey()
	cv2.destroyAllWindows()

Main()
