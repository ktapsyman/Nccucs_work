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
		"""
		This image is a bilevel image! I've dealt with it 
		test = searchImageByName("ukbench00472.jpg", Images)
		print(r)
		print(g)
		print(b)
		print test.getColorHistogram()
		"""
	
	def cleanUp(self):
		for img in self.allImages:
			img.close()

	def initUI(self):
	  
		self.parent.title("HW3") 

		self.pack(fill=BOTH, expand=True)

		Label(self, font=("Courier", 14, "bold"), text = "Select File: ").grid(row=0, column=0, pady=5)
		Button(self, text = "Click to select file", command = lambda : openFile(self)).grid(row=0, column=1, pady=5)
		self.fileName = StringVar()
		Label(self, textvariable=self.fileName, font=("Courier", 14)).grid(row=0, column=1, columnspan=2, pady=5, sticky=W)

		Label(self, text = "Select Mode: ", font=("Courier", 14, "bold")).grid(row=1, column=0, pady=5)
		mode = StringVar(self)
		mode.set("Q1-ColorHistogram")
		om = OptionMenu(self, mode, "Q1-ColorHistogram", "Q2-ColorLayout", "Q3-SIFT Visual Words", "Q4-Visual Words using stop words" )
		om.grid(row=1, column=1, pady=5, sticky=W)

		Button(self, text = "SEARCH!", command = lambda: startSearching(self, self.fileName.get(),mode.get())).grid(row=3, column=1, pady=5)
		
		for col in range(5):
			titleLbl = Label(self, text=TITLE[col], font=("Courier", 14, "bold")).grid(row=4, column=col, padx=50)
		
		self.images = []
		for rowCount in range(10):
			for colCount in range(5):
				self.images.append(Label(self, text="Test row="+str(rowCount) + " col=" + str(colCount)))
				self.images[rowCount*5+colCount].grid(row=rowCount+5, column=colCount, pady=20, padx=5)
	
	def updateImgList(self, imgList):
		for rowCount in range(10):
			for colCount in range(5):
				self.images[rowCount*5+colCount].configure(image=None)
		
		
def searchImageByName(fileName, imgList):
	print(fileName)
	for img in imgList:
		if img.getFileName() == fileName:
			return img
	return None

def getTop10SimilarColorHist(img, imgList):
	targetHist = img.getColorHistogram()
	print targetHist.shape
	print imgList[10].getColorHistogram().shape
	for image in imgList:
		print image.getFileName()
		print image.getColorHistogram().shape
	top10ColorHist = [(image, l2Norm(targetHist, image.getColorHistogram())) for image in imgList]#.sort(key=lambda x : x[1])
	return top10ColorHist

def startSearching (app, fileName, mode):
	imgList = []
	targetImg = searchImageByName(fileName, app.allImages)
	if mode == "Q1-ColorHistogram":
		if 0 != len(targetImg.getMetricResult(mode)):
			imgList	= targetImg.getMetricResult[mode]
		else:
			imgList = getTop10SimilarColorHist(targetImg, app.allImages)
			targetImage.setMetricResult(mode, imgList)
			print imgList
		print mode
	elif mode == "Q2-ColorLayout":
		print mode
	elif mode == "Q3-SIFT Visual Words":
		print mode
	elif mode == "Q4-Visual Words using stop words":
		print mode
	
	app.updateImgList(imgList)
	

if __name__ == '__main__':
	root = Tk()
	size = 720, 1024

	app = Example(root)
	app.setAllImages([customizedImage(img, Image.open("./dataset/"+img)) for img in os.listdir("./dataset") if ".jpg" in img])
	root.geometry("1024x720")
	root.mainloop()
	app.cleanUp()

  
