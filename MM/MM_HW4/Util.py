"""
Author : 106753027 Jung, Liang@NCCUCS
Environment:
	OS : MacOS Sierra
	Python : 2.7.10
"""
import os
from copy import deepcopy
import csv

import numpy as np
from scipy.fftpack import dct
from sklearn.cluster import KMeans
import sift

from Tkinter import *
import tkFileDialog 
import tkMessageBox
from ttk import Frame, Button, Label, Style

from PIL import ImageTk, Image


class customizedImage(object):
	def __init__(self, fileName, img):
		self._img = img#.resize((224, 256))
		self._fileName = fileName

		histogram = self._img.histogram()
		if 256 == len(histogram):
			newImg = Image.new("RGB", self._img.size)
			newImg.paste(self._img)
			self._img = newImg
			newImg.save("./dataset/"+fileName)

		SIFTFilename = "./SIFT/"+fileName.split(".")[0]+".sift"
		if not os.path.isfile(SIFTFilename):
			sift.process_image("./dataset/"+fileName, SIFTFilename)

		self._colorHistogram = np.array(self._img.histogram())
		self._colorLayout = None#getColorLayout(self._img, fileName)
		pos, descriptors = sift.read_features_from_file(SIFTFilename)
		self.SIFTDescriptors = descriptors
		self.SIFTEnc = {}#Encoded visual words
		self.SIFTVisualWords = None
		self.SIFTWithoutStopWords = None
	
	def show(self):
		self._img.show()

	def close(self):
		self._img.close()
	
	def getFileName(self):
		return self._fileName
	
	def getColorHistogram(self):
		return self._colorHistogram

	def getColorLayout(self):
		return self._colorLayout
	
	def getSIFTDescriptors(self):
		return self.SIFTDescriptors

	def getSIFTVisualWords(self):
		return self.SIFTVisualWords

	def getSIFTEncoding(self):
		return self.SIFTEnc
	
	def getSIFTWithoutStopWords(self):
		return self.SIFTWithoutStopWords
	
	def setSIFTEncoding(self, enc):
		self.SIFTEnc = enc
	
	def setSIFTVisualWords(self, visualWords):
		self.SIFTVisualWords = visualWords
	
	def setSIFTWithoutStopWords(self, visualWordsWithoutStopWords):
		self.SIFTWithoutStopWords = visualWordsWithoutStopWords
	
	def toMosaic(self, candidates, blockWidth, blockHeight):
		imageBlocks = splitImageToBlocks(self, blockWidth, blockHeight)
		for block in imageBlocks:
			continue
		mosaicImg = composeImg()

def splitImageToBlocks(img, blockWidth, blockHeight):
	#TODO
	return []

def zigZag(array, row, col):
	wPos = 0
	hPos = 0
	direction = 1
	ret = []
	while wPos != col-1 or hPos != row-1:
		ret.append(array[row*hPos+wPos])

		if (hPos == 0 or hPos == col-1) and wPos%2 == 0:
			wPos += 1
			direction *= -1

		elif (wPos == 0 or wPos == row-1) and hPos%2 == 1:
			direction *= -1
			hPos += 1

		else:
			wPos += direction
			hPos -= direction
	ret.append(array[-1])
	return ret
			

def getColorLayout(img, fileName):
	width, height = img.size
	blockWidth = width/8
	blockHeight = height/8
	partitions = []
	for row in xrange(0, height, blockHeight):
		for col in xrange(0, width, blockWidth):
			imgSlice = img.crop((row, col, row+blockHeight, col+blockWidth))
			partition = np.array(imgSlice)
			representativeIcon = partition.mean(axis=(0, 1))
			imgSlice.paste((int(representativeIcon[0]), int(representativeIcon[1]), int(representativeIcon[2])), (0, 0, imgSlice.size[0], imgSlice.size[1]))
			imgSlice = np.array(imgSlice.convert("YCbCr"))
			dctY = dct(imgSlice[0])
			dctCb = dct(imgSlice[1])
			dctCr = dct(imgSlice[2])
			partitions.append((dctY, dctCb, dctCr))
	ret = (np.array(zigZag([x[0] for x in partitions], 8, 8)), np.array(zigZag([x[1] for x in partitions], 8, 8)), np.array(zigZag([x[2] for x in partitions], 8, 8)))
	return ret

def searchBestCandidate (img, imgList, mode):
	bestCandidate = None
	if mode == "ColorHistogram":
		bestCandidate = getMostSimilarColorHist(img, imgList)
	
	elif mode == "ColorLayout":
		bestCandidate = getMostSimilarColorLayout(targetImg, app.allImages)
	
	elif mode == "SIFT Visual Words":
		bestCandidate = getMostSimilarSIFT(targetImg, app.allImages)

	elif mode == "Visual Words using stop words":
		bestCandidate = getMostSimilarSIFTWithoutStopWords(targetImg, app.allImages)
		

def getMostSimilarColorHist(img, imgList):
	targetHist = img.getColorHistogram()
	topColorHist = []

	topColorHist = [(image, l2Norm(targetHist, image.getColorHistogram())) for image in imgList]
	topColorHist.sort(key=lambda x:x[1])

	return topColorHist[0]

def getMostSimilarColorLayout(img, imgList):
	targetColorLayout = img.getColorLayout()
	topColorLayout = []

	topColorLayout = [(image, 0.8*l2Norm(targetColorLayout[0], image.getColorLayout()[0])+0.1*l2Norm(targetColorLayout[1], image.getColorLayout()[1])+0.1*l2Norm(targetColorLayout[2], image.getColorLayout()[2])) for image in imgList]
	topColorLayout.sort(key=lambda x:x[1])

	return topColorLayout[0]

def getMostSimilarSIFT(img, imgList):
	targetSIFT = img.getSIFTVisualWords()
	topSIFT = []

	topSIFT = [(image, l2Norm(targetSIFT, image.getSIFTVisualWords())) for image in imgList]
	topSIFT.sort(key=lambda x:x[1])
		
	return top10SIFT[0]

def getMostSimilarSIFTWithoutStopWords(img, imgList):
	targetSIFT = img.getSIFTWithoutStopWords()
	topSIFT = []

	topSIFT = [(image, l2Norm(targetSIFT, image.getSIFTWithoutStopWords())) for image in imgList]
	topSIFT.sort(key=lambda x:x[1])

	return topSIFT[0]

def openFile (app):
	fileName = tkFileDialog.askopenfilename(initialdir = "./dataset")
	app.fileName.set(os.path.split(fileName)[1])
	app.currentImg = customizedImage(fileName, Image.open(fileName))
	print fileName


def l2Norm(vec1, vec2):
	return np.linalg.norm(vec2-vec1)
