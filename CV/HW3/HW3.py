import cv2

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

def Q1():
	Img = cv2.imread("hw3.jpg", cv2.IMREAD_GRAYSCALE)
	CDF = CalculateCDFFrom2DPixels(Img)
	CDFMin = list(CDF)[0]
	HistogramEqualizer = CreateHistogramEqualizer(CDFMin, Img.size)

	cv2.imshow("Before", Img)

	Height, Width = Img.shape
	for Row in range(0, Height):
		for Col in range(0, Width):
			Img[Row][Col] = HistogramEqualizer(CDF[Img[Row][Col]])
	
	cv2.imshow("After", Img)
	return

def Q2():
	Q2a()
	Q2b()
	Q2c()

	return

def Q2a():
	return

def Q2b():
	return

def Q2c():
	return

def Main():
	Q1()
	Q2()
	cv2.waitKey()
	cv2.destroyAllWindows()

Main()
