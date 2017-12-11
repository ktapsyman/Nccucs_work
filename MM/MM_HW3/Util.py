"""
Author : 106753027 Jung, Liang@NCCUCS
Environment:
	OS : MacOS Sierra
	Python : 2.7.10
"""
from PIL import Image
import numpy as np

class customizedImage(object):
	def __init__(self, img):
		self._img = img
		self.colorHistogram = np.array(img.histogram())
		self.colorLayout = getColorLayout(img)
		self.SIFT = None #TODO
	def show(self):
		self._img.show()

	def close(self):
		self._img.close()

def openFile ():
	fileName = tkFileDialog.askopenfilename(initialdir = "./dataset")
	app.fileName.set(fileName)

def getColorLayout(img):
	#TODO
	return None

def l2Norm(vec1, vec2):
	return np.linalg.norm(vec2-vec1)
