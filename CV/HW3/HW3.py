import cv2
import numpy as np

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
	HistogramEqualizer = lambda CDFofPixel: round((CDFofPixel-CDFMin)*(GrayScaleLevel-1)/(ImgSize-1))

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

def ShowComparison(Title, OriginalImg, EqualizedImg):
	if Title is None or 0 == len(Title):
		Title = "Default Title"
	
	ComparisonImg = np.hstack((OriginalImg, EqualizedImg))
	cv2.imshow(Title, ComparisonImg)

def Q1():
	Img = cv2.imread("hw3.jpg", cv2.IMREAD_GRAYSCALE)
	EqualizedImg = HistogramEqualize(Img.copy())
	
	ShowComparison("Q1", Img, EqualizedImg)
	return

def Q2():
	Img = cv2.imread("hw3a.jpg", cv2.IMREAD_COLOR)
	Q2a(Img.copy())
	Q2b(Img.copy())
	Q2c(Img.copy())

	return

def Q2a(Img):
	BChannel, GChannel, RChannel = cv2.split(Img)

	# B
	EqualizedBChannel = HistogramEqualize(BChannel)

	# G
	EqualizedGChannel = HistogramEqualize(GChannel)

	# R
	EqualizedRChannel = HistogramEqualize(RChannel)
	
	EqualizedImg = cv2.merge((EqualizedBChannel, EqualizedGChannel, EqualizedRChannel))
	ShowComparison("Q2a", Img, EqualizedImg)
	return

def Q2b(Img):
	Img = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)
	HChannel, SChannel, VChannel = cv2.split(Img)

	EqulizedVChannel = HistogramEqualize(VChannel)

	EqualizedImg = cv2.merge((HChannel, SChannel, EqulizedVChannel))
	ShowComparison("Q2b", Img, EqualizedImg)

	return

def Q2c(Img):
	Img = cv2.cvtColor(Img, cv2.COLOR_BGR2YCR_CB)
	YChannel, CbChannel, CrChannel = cv2.split(Img)

	EqulizedYChannel = HistogramEqualize(YChannel)

	EqualizedImg = cv2.merge((EqulizedYChannel, CbChannel, CrChannel))
	ShowComparison("Q2c", Img, EqualizedImg)
	return

def Main():
	Q1()
	Q2()
	cv2.waitKey()
	cv2.destroyAllWindows()

Main()
