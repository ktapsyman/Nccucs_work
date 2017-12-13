"""
Author : 106753027 Jung, Liang@NCCUCS
Environment:
	OS : MacOS Sierra
	Python : 2.7.10
"""
import os
import numpy as np
from scipy.fftpack import dct

from Tkinter import *
import tkFileDialog 
import tkMessageBox
from ttk import Frame, Button, Label, Style

from PIL import ImageTk, Image

class customizedImage(object):
	def __init__(self, fileName, img):
		self._img = img.resize((224, 256))
		self._fileName = fileName

		histogram = self._img.histogram()
		if 256 == len(histogram):
			newImg = Image.new("RGB", self._img.size)
			newImg.paste(self._img)
			self._img = newImg
		
		self._colorHistogram = np.array(self._img.histogram())
		self._colorLayout = getColorLayout(self._img, fileName)
		self.MetricDic = {"Q1-ColorHistogram":[], "Q2-ColorLayout":[], "Q3-SIFT Visual Words":[], "Q4-Visual Words using stop words":[]}
		self.SIFTVisualWords = None #TODO
		self.SIFTWithStopWords = None #TODO
	
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
	
	def getSIFTVisualWords(self):
		return self.SIFTVisualWords	
	
	def getSIFTWithStopWords(self):
		return self.SIFTWithStopWords
	
	def getMetricResult(self, metric=""):
		return self.MetricDic[metric]	
	
	def setMetricResult(self, metricResult, metric="" ):#Top 10 only
		self.MetricDic[metric] = metricResult

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
	for row in range(0, height, blockHeight):
		for col in range(0, width, blockWidth):
			imgSlice = img.crop((row, col, row+blockHeight, col+blockWidth))
			partition = np.array(imgSlice)
			representativeIcon = partition.mean(axis=(0, 1))
			imgSlice.paste((int(representativeIcon[0]), int(representativeIcon[1]), int(representativeIcon[2])), (0, 0, imgSlice.size[0], imgSlice.size[1]))
			imgSlice = np.array(imgSlice.convert("YCbCr"))
			dctY = imgSlice[0]
			dctCb = imgSlice[1]
			dctCr = imgSlice[2]
			partitions.append((dctY, dctCb, dctCr))
	ret = (np.array(zigZag([x[0] for x in partitions], 8, 8)), np.array(zigZag([x[1] for x in partitions], 8, 8)), np.array(zigZag([x[2] for x in partitions], 8, 8)))
	if (64, 31, 3) == ret[0].shape or (64, 31, 3) == ret[1].shape or (64, 31, 3) == ret[2].shape:
		print fileName
		print ret[0].shape
		print ret[1].shape
		print ret[2].shape
		print "===================================="
	return ret

def openFile (app):
	fileName = tkFileDialog.askopenfilename(initialdir = "./dataset")
	app.fileName.set(os.path.split(fileName)[1])


def l2Norm(vec1, vec2):
	return np.linalg.norm(vec2-vec1)
