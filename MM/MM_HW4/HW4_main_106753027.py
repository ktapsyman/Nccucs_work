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
		self.currentImg = None

	def setAllImages(self, Images):
		self.allImages = Images
		"""
		allSIFT = []
		
		for img in self.allImages:
			currentDesc = [desc for desc in img.getSIFTDescriptors()]
			allSIFT += currentDesc
		index = 0
		nClusters = 20
		allEncDict = dict((x, 0) for x in xrange(nClusters))

		kMeans = KMeans(n_clusters=nClusters).fit_predict(np.array(allSIFT))
		for img in self.allImages:
			descLen = len(img.getSIFTDescriptors())
			currentLabels = kMeans[index:index+descLen]
			enc = dict((x, 0) for x in xrange(nClusters))
			for label in currentLabels:
				enc[label] += 1
				allEncDict[label] += 1
			img.setSIFTEncoding(enc)
			img.setSIFTVisualWords(np.array(enc.values()))
			index += descLen

		topStopWords = sorted(allEncDict.items(), key=lambda x : x[1], reverse=True)[:int(nClusters/10)]
		for img in self.allImages:
			visualWordsWithoutStopWords = deepcopy(img.getSIFTEncoding())
			for stopWord in topStopWords:
				visualWordsWithoutStopWords.pop(stopWord[0], None)
			img.setSIFTWithoutStopWords(np.array(visualWordsWithoutStopWords.values()))
		"""

	def cleanUp(self):
		for img in self.allImages:
			img.close()

	def initUI(self):
	  
		self.parent.title("HW4 Image Mosaic") 

		self.pack(fill=BOTH, expand=True)

		Label(self, font=("Courier", 12, "bold"), text = "Select File: ").grid(row=0, column=0, pady=5)
		Button(self, text = "Click to select file", command = lambda : openFile(self)).grid(row=0, column=1, pady=5)
		self.fileName = StringVar()
		Label(self, textvariable=self.fileName, font=("Courier", 12)).grid(row=0, column=2, columnspan=2, pady=5, sticky=W)

		Label(self, text = "Select Mode: ", font=("Courier", 12, "bold")).grid(row=1, column=0, pady=5)
		mode = StringVar(self)
		mode.set("ColorHistogram")
		om = OptionMenu(self, mode, "ColorHistogram", "ColorLayout", "SIFT Visual Words", "Visual Words using stop words" )
		om.grid(row=1, column=1, pady=5, sticky=W)

		Button(self, text = "Mosiac!", command = lambda: startSearching(self, self.fileName.get(),mode.get())).grid(row=3, column=1, pady=5)
		
		for col in xrange(5):
			titleLbl = Label(self, text=TITLE[col], font=("Courier", 12, "bold")).grid(row=4, column=col, padx=50)
		
		self.images = []
		for rowCount in xrange(2):
			for colCount in xrange(2):
				self.images.append(Label(self))
				self.images[rowCount*2+colCount].grid(row=rowCount+5, column=colCount, pady=5, padx=5)
	"""
	def updateImgList(self, metric, imgList):
		for rowCount in xrange(10):
			img = ImageTk.PhotoImage(Image.open("./dataset/"+imgList[rowCount][0].getFileName()).resize((50, 50), Image.ANTIALIAS))
			self.images[rowCount*5].configure(text=rowCount+1)
			self.images[rowCount*5+1].configure(text=imgList[rowCount][0].getFileName())
			self.images[rowCount*5+2].configure(image=img)
			self.images[rowCount*5+2].image = img
			self.images[rowCount*5+3].configure(text=metric)
			self.images[rowCount*5+4].configure(text=imgList[rowCount][1])
	"""

if __name__ == '__main__':
	root = Tk()
	size = 800, 1280

	app = Example(root)
	app.setAllImages([customizedImage(img, Image.open("./dataset/"+img)) for img in os.listdir("./dataset") if ".jpg" in img])
	root.geometry("1280x800")
	root.mainloop()
	app.cleanUp()

  
