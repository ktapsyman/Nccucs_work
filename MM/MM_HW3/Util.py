"""
Author : 106753027 Jung, Liang@NCCUCS
Environment:
	OS : MacOS Sierra
	Python : 2.7.10
"""
import os
import numpy as np

from Tkinter import *
import tkFileDialog 
import tkMessageBox
from ttk import Frame, Button, Label, Style

from PIL import ImageTk, Image

class customizedImage(object):
	def __init__(self, fileName, img):
		self._img = img
		self._fileName = fileName
		self._colorHistogram = np.array(img.histogram())
		self._colorLayout = getColorLayout(img)
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

def getColorLayout(img):
	#TODO
	return None

def openFile (app):
	fileName = tkFileDialog.askopenfilename(initialdir = "./dataset")
	app.fileName.set(os.path.split(fileName)[1])


def l2Norm(vec1, vec2):
	if 256 == vec1.shape[0] or 256 == vec2.shape[0]:
		print 256
	return np.linalg.norm(vec2-vec1)
