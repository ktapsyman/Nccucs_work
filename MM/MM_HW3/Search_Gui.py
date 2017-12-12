"""
Author : 106753027 Jung, Liang@NCCUCS
Environment:
	OS : MacOS Sierra
	Python : 2.7.10
"""
from pylab import *
from Util import *

TITLE = ["Rank", "Filename", "Image", "Metric", "Similarity"]

class Example(Frame):
  
	def __init__(self, parent):
		Frame.__init__(self, parent)   
		self.parent = parent
		self.initUI()

	def setAllImages(self, Images):
		self.allImages = Images
	
	def cleanUp(self):
		for img in self.allImages:
			img.close()

	def initUI(self):
	  
		self.parent.title("HW3") 

		self.pack(fill=BOTH, expand=True)

		Label(self, font=("Courier", 12, "bold"), text = "Select File: ").grid(row=0, column=0, pady=5)
		Button(self, text = "Click to select file", command = lambda : openFile(self)).grid(row=0, column=1, pady=5)
		self.fileName = StringVar()
		Label(self, textvariable=self.fileName, font=("Courier", 12)).grid(row=0, column=1, columnspan=2, pady=5, sticky=W)

		Label(self, text = "Select Mode: ", font=("Courier", 12, "bold")).grid(row=1, column=0, pady=5)
		mode = StringVar(self)
		mode.set("Q1-ColorHistogram")
		om = OptionMenu(self, mode, "Q1-ColorHistogram", "Q2-ColorLayout", "Q3-SIFT Visual Words", "Q4-Visual Words using stop words" )
		om.grid(row=1, column=1, pady=5, sticky=W)

		Button(self, text = "SEARCH!", command = lambda: startSearching(self, self.fileName.get(),mode.get())).grid(row=3, column=1, pady=5)
		
		for col in range(5):
			titleLbl = Label(self, text=TITLE[col], font=("Courier", 12, "bold")).grid(row=4, column=col, padx=50)
		
		self.images = []
		for rowCount in range(10):
			for colCount in range(5):
				self.images.append(Label(self))
				self.images[rowCount*5+colCount].grid(row=rowCount+5, column=colCount, pady=5, padx=5)
	
	def updateImgList(self, metric, imgList):
		for rowCount in range(10):
			img = ImageTk.PhotoImage(Image.open("./dataset/"+imgList[rowCount][0].getFileName()).resize((50, 50), Image.ANTIALIAS))
			self.images[rowCount*5].configure(text=rowCount+1)
			self.images[rowCount*5+1].configure(text=imgList[rowCount][0].getFileName())
			self.images[rowCount*5+2].configure(image=img)
			self.images[rowCount*5+2].image = img
			self.images[rowCount*5+3].configure(text=metric)
			self.images[rowCount*5+4].configure(text=imgList[rowCount][1])

def searchImageByName(fileName, imgList):
	for img in imgList:
		if img.getFileName() == fileName:
			return img
	return None

def getTop10SimilarColorHist(img, imgList):
	targetHist = img.getColorHistogram()
	top10ColorHist = [(image, l2Norm(targetHist, image.getColorHistogram())) for image in imgList]
	top10ColorHist.sort(key=lambda x:x[1])
	return top10ColorHist[:10]

def getTop10SimilarColorLayout(img, imgList):
	targetColorLayout = img.getColorLayout()
	return None #TODO

def startSearching (app, fileName, mode):
	imgList = []
	targetImg = searchImageByName(fileName, app.allImages)
	
	if 0 != len(targetImg.getMetricResult(mode)):
		imgList	= targetImg.getMetricResult[mode]
	else:
		if mode == "Q1-ColorHistogram":
			imgList = getTop10SimilarColorHist(targetImg, app.allImages)
		elif mode == "Q2-ColorLayout":
			print mode
		elif mode == "Q3-SIFT Visual Words":
			print mode
		elif mode == "Q4-Visual Words using stop words":
			print mode
		targetImg.setMetricResult(imgList, metric=mode)
	
	app.updateImgList(mode, imgList)

if __name__ == '__main__':
	root = Tk()
	size = 800, 1280

	app = Example(root)
	app.setAllImages([customizedImage(img, Image.open("./dataset/"+img)) for img in os.listdir("./dataset") if ".jpg" in img])
	root.geometry("1280x800")
	root.mainloop()
	app.cleanUp()

  
