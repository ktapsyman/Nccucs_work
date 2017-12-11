"""
Author : 106753027 Jung, Liang@NCCUCS
Environment:
	OS : MacOS Sierra
	Python : 2.7.10
"""
import os
from pylab import *

import pickle

from Tkinter import *
from PIL import ImageTk, Image
import tkMessageBox
import tkFileDialog 
from ttk import Frame, Button, Label, Style

from Util import *


class Example(Frame):
  
	def __init__(self, parent):
		Frame.__init__(self, parent)   
		self.parent = parent
		self.initUI()

	def setAllImages(self, Images):
		self.allImages = Images
		Images[0][1].show()
		print l2Norm(Images[0][1].colorHistogram, Images[1][1].colorHistogram)
		for i in range(10):
			continue
	
	def cleanUp(self):
		for img in self.allImages:
			img[1].close()

	def initUI(self):
	  
		self.parent.title("HW3") 

		self.pack(fill=BOTH, expand=1)

		Button(self, text = "Select File", command = openFile).grid(row=0, column=0, pady=5)
		self.fileName = StringVar()
		Label(self, textvariable=self.fileName).grid(row=0, column=1, columnspan=2, pady=5, sticky=W)

		Label(self, text = "Select Mode: ").grid(row=1, column=0, pady=5)
		mode = StringVar(self)
		mode.set("Q1-ColorHistogram")
		om = OptionMenu(self, mode, "Q1-ColorHistogram", "Q2-ColorLayout", "Q3-SIFT Visual Words", "Q4-Visual Words using stop words")
		om.grid(row=1, column=1, pady=5, sticky=W)

		Button(self, text = "SEARCH", command = lambda: startSearching(self.fileName.get(),mode.get())).grid(row=3, column=0, pady=5)

		self.images = []
		for i in range(10):
			self.images.append(Label(self, text="Test"+str(i)))
			self.images[i].grid(row=i/5+4, column=i%5, pady=50)
 

def startSearching (fileName, mode):
	if mode == "Q1-ColorHistogram":
		print mode
	elif mode == "Q2-ColorLayout":
		print mode
	elif mode == "Q3-SIFT Visual Words":
		print mode
	elif mode == "Q4-Visual Words using stop words":
		print mode
	

if __name__ == '__main__':
	root = Tk()
	size = 220, 220

	app = Example(root)
	app.setAllImages([(img, customizedImage(Image.open("./dataset/"+img))) for img in os.listdir("./dataset") if ".jpg" in img])
	root.geometry("1024x720")
	root.mainloop()
	app.cleanUp()

  
