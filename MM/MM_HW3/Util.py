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
		self._img = img
		self._fileName = fileName

		histogram = self._img.histogram()
		if 256 == len(histogram):
			newImg = Image.new("RGB", img.size)
			newImg.paste(img)
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

def getColorLayout(img, fileName):
	width, height = img.size
	blockWidth = width/8
	blockHeight = height/8
	partitions = []
	for row in range(0, height-blockHeight, blockHeight):
		for col in range(0, width-blockWidth, blockWidth):
			#TODO : representitive color : average
			partition = np.array(img.crop((row, col, row+blockHeight, col+blockWidth)))
			print partition.shape
			partitions.append((dctY, dctCb, dctCr))
	return None

def openFile (app):
	fileName = tkFileDialog.askopenfilename(initialdir = "./dataset")
	app.fileName.set(os.path.split(fileName)[1])


def l2Norm(vec1, vec2):
	return np.linalg.norm(vec2-vec1)
