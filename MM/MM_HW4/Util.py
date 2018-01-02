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

BLOCK_SIZE_LIST = [5, 10, 20, 40, 80]

class ImageWithCache(object):
	def __init__(self, img):
		self.img = img

		weight, height = self.img.size

		self.metricDic = {"ColorHistogram":{}, "ColorLayout":{}}
		
		for blockSize in BLOCK_SIZE_LIST:
			currentSizeImg = img.resize((weight/blockSize, height/blockSize))
			self.metricDic["ColorHistogram"][blockSize] = getColorHistogram(currentSizeImg)
			self.metricDic["ColorLayout"][blockSize] = getColorLayout(currentSizeImg)
	def close(self):
		self.img.close()

def splitImageToBlocks(img, blockSize):
	width, height = img.size
	blockWidth = width/blockSize
	blockHeight = height/blockSize
	
	retImgBlocks = []

	for row in xrange(blockSize):
		retImgBlocks.append([])
		for col in xrange(blockSize):
			retImgBlocks[row].append(img.crop((col*blockWidth, row*blockHeight, (col+1)*blockWidth, (row+1)*blockHeight)))
	return retImgBlocks

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
			
def getColorHistogram(img):
	return np.array(img.histogram())

def getColorLayout(img):
	width, height = img.size
	if width < 8:
		if height < 8:
			img = img.resize((8, 8))
		else:
			img = img.resize((8, height))
	elif height < 8:
		img = img.resize((width, 8))
		
	width, height = img.size
	blockWidth = width/8
	blockHeight = height/8
	partitions = []

	for row in xrange(0, height, blockHeight):
		for col in xrange(0, width, blockWidth):
			imgSlice = img.crop((col, row, col+blockWidth, row+blockHeight))
			partition = np.array(imgSlice)
			representativeIcon = partition.mean(axis=(0, 1))
			imgSlice.paste((int(representativeIcon[0]), int(representativeIcon[1]), int(representativeIcon[2])), (0, 0, imgSlice.size[0], imgSlice.size[1]))

			imgSlice = imgSlice.convert("YCbCr")
			Y, Cb, Cr = imgSlice.split()
			dctY = dct(Y)
			dctCb = dct(Cb)
			dctCr = dct(Cr)
			partitions.append((dctY, dctCb, dctCr))

	colorLayout = (np.array(zigZag([x[0] for x in partitions], 8, 8)), np.array(zigZag([x[1] for x in partitions], 8, 8)), np.array(zigZag([x[2] for x in partitions], 8, 8)))

	return np.array(colorLayout)

def searchBestCandidate (img, imgList, mode, blockSize):
	bestCandidate = None
	if mode == "ColorHistogram":
		bestCandidate = getMostSimilarColorHist(img, imgList, blockSize)
	
	elif mode == "ColorLayout":
		bestCandidate = getMostSimilarColorLayout(img, imgList, blockSize)
	
	return bestCandidate

def getMostSimilarColorHist(img, imgDataset, blockSize):
	targetHist = getColorHistogram(img)

	topColorHist = [(imageContainer.img, l2Norm(targetHist, imageContainer.metricDic["ColorHistogram"][blockSize])) for imageContainer in imgDataset]
	topColorHist.sort(key=lambda x:x[1])

	return topColorHist[0][0]

def getMostSimilarColorLayout(img, imgDataset, blockSize):
	targetColorLayout = getColorLayout(img)
	topColorLayout = []

	for imageContainer in imgDataset:
		currentColorLayout = imageContainer.metricDic["ColorLayout"][blockSize]
		topColorLayout.append((imageContainer.img, 
		0.8*l2Norm(targetColorLayout[0], currentColorLayout[0])+
		0.1*l2Norm(targetColorLayout[1], currentColorLayout[1])+
		0.1*l2Norm(targetColorLayout[2], currentColorLayout[2])))

	topColorLayout.sort(key=lambda x:x[1])

	return topColorLayout[0][0]

def openFile (app):
	fileName = tkFileDialog.askopenfilename(initialdir = "./dataset")
	app.fileName.set(os.path.split(fileName)[1])
	app.currentImg = Image.open(fileName).resize((640, 480))

	tkImg = ImageTk.PhotoImage(app.currentImg, Image.ANTIALIAS)
	app.imgContainer["Original"].configure(image=tkImg)
	app.imgContainer["Original"].image = tkImg


def l2Norm(vec1, vec2):
	return np.linalg.norm(vec2-vec1)
