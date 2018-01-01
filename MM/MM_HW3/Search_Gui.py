"""
Author : 106753027 Jung, Liang@NCCUCS
Environment:
	OS : Ubuntu 16.04 LTS
	Python : 2.7.12
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

	def cleanUp(self):
		for img in self.allImages:
			img.close()

	def initUI(self):
	  
		self.parent.title("HW3") 

		self.pack(fill=BOTH, expand=True)

		Label(self, font=("Courier", 12, "bold"), text = "Select File: ").grid(row=0, column=0, pady=5)
		Button(self, text = "Click to select file", command = lambda : openFile(self)).grid(row=0, column=1, pady=5)
		self.fileName = StringVar()
		Label(self, textvariable=self.fileName, font=("Courier", 12)).grid(row=0, column=2, columnspan=2, pady=5, sticky=W)

		Label(self, text = "Select Mode: ", font=("Courier", 12, "bold")).grid(row=1, column=0, pady=5)
		mode = StringVar(self)
		mode.set("Q1-ColorHistogram")
		om = OptionMenu(self, mode, "Q1-ColorHistogram", "Q2-ColorLayout", "Q3-SIFT Visual Words", "Q4-Visual Words using stop words" )
		om.grid(row=1, column=1, pady=5, sticky=W)

		Button(self, text = "SEARCH!", command = lambda: startSearching(self, self.fileName.get(),mode.get())).grid(row=3, column=1, pady=5)
		
		for col in xrange(5):
			titleLbl = Label(self, text=TITLE[col], font=("Courier", 12, "bold")).grid(row=4, column=col, padx=50)
		
		self.images = []
		for rowCount in xrange(10):
			for colCount in xrange(5):
				self.images.append(Label(self))
				self.images[rowCount*5+colCount].grid(row=rowCount+5, column=colCount, pady=5, padx=5)
	
	def updateImgList(self, metric, imgList):
		for rowCount in xrange(10):
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

def searchClothSubsetByType(imglist, clothType):
	return filter(lambda x : x.getClothType()==clothType, imglist)

def createQuerySet(imgSubset, imgList):
	return [x for x in imgList if x not in imgSubset]

def getTop10SimilarColorHist(img, imgList):
	targetHist = img.getColorHistogram()
	top10ColorHist = []

	targetSubset = searchClothSubsetByType(imgList, img.getClothType())
	if len(targetSubset) >= 10:
		top10ColorHist = [(image, l2Norm(targetHist, image.getColorHistogram())) for image in targetSubset]
		top10ColorHist.sort(key=lambda x:x[1])
	else:
		querySet = createQuerySet(targetSubset, imgList)
		top10ColorHist = sorted([(image, l2Norm(targetHist, image.getColorHistogram())) for image in targetSubset], key=lambda x:x[1]) + sorted([(image, l2Norm(targetHist, image.getColorHistogram())) for image in querySet], key=lambda x:x[1])[:10-len(targetSubset)]

	return top10ColorHist[:10]

def getTop10SimilarColorLayout(img, imgList):
	targetColorLayout = img.getColorLayout()
	top10ColorLayout = []

	targetSubset = searchClothSubsetByType(imgList, img.getClothType())
	if len(targetSubset) >= 10:
		top10ColorLayout = [(image, 0.8*l2Norm(targetColorLayout[0], image.getColorLayout()[0])+0.1*l2Norm(targetColorLayout[1], image.getColorLayout()[1])+0.1*l2Norm(targetColorLayout[2], image.getColorLayout()[2])) for image in targetSubset]
		top10ColorLayout.sort(key=lambda x:x[1])
	else:
		querySet = createQuerySet(targetSubset, imgList)
		top10ColorLayout = sorted([(image, 0.8*l2Norm(targetColorLayout[0], image.getColorLayout()[0])+0.1*l2Norm(targetColorLayout[1], image.getColorLayout()[1])+0.1*l2Norm(targetColorLayout[2], image.getColorLayout()[2])) for image in targetSubset], key=lambda x:x[1])+sorted([(image, 0.8*l2Norm(targetColorLayout[0], image.getColorLayout()[0])+0.1*l2Norm(targetColorLayout[1], image.getColorLayout()[1])+0.1*l2Norm(targetColorLayout[2], image.getColorLayout()[2])) for image in querySet], key=lambda x:x[1])[:10-len(targetSubset)]

	return top10ColorLayout[:10]

def getTop10SIFT(img, imgList):
	targetSIFT = img.getSIFTVisualWords()
	top10SIFT = []

	targetSubset = searchClothSubsetByType(imgList, img.getClothType())
	if len(targetSubset) >= 10:
		top10SIFT = [(image, l2Norm(targetSIFT, image.getSIFTVisualWords())) for image in targetSubset]
		top10SIFT.sort(key=lambda x:x[1])
	else:
		querySet = createQuerySet(targetSubset, imgList)
		top10SIFT = sorted([(image, l2Norm(targetSIFT, image.getSIFTVisualWords())) for image in targetSubset], key=lambda x:x[1]) + sorted([(image, l2Norm(targetSIFT, image.getSIFTVisualWords())) for image in querySet])[:10-len(targetSubset)]
		
	return top10SIFT[:10]

def getTop10SIFTWithoutStopWords(img, imgList):
	targetSIFT = img.getSIFTWithoutStopWords()
	top10SIFT = []

	targetSubset = searchClothSubsetByType(imgList, img.getClothType())
	if len(targetSubset) >= 10:
		top10SIFT = [(image, l2Norm(targetSIFT, image.getSIFTWithoutStopWords())) for image in targetSubset]
		top10SIFT.sort(key=lambda x:x[1])
	else:
		querySet = createQuerySet(targetSubset, imgList)
		top10SIFT = sorted([(image, l2Norm(targetSIFT, image.getSIFTWithoutStopWords())) for image in targetSubset], key=lambda x:x[1]) + sorted([(image, l2Norm(targetSIFT, image.getSIFTWithoutStopWords())) for image in querySet])[:10-len(targetSubset)]

	return top10SIFT[:10]

def startSearching (app, fileName, mode):
	imgList = []
	targetImg = searchImageByName(fileName, app.allImages)
	if 0 != len(targetImg.getMetricResult(mode)):
		imgList	= targetImg.getMetricResult(mode)
	else:
		if mode == "Q1-ColorHistogram":
			imgList = getTop10SimilarColorHist(targetImg, app.allImages)
		
		elif mode == "Q2-ColorLayout":
			imgList = getTop10SimilarColorLayout(targetImg, app.allImages)
		
		elif mode == "Q3-SIFT Visual Words":
			imgList = getTop10SIFT(targetImg, app.allImages)

		elif mode == "Q4-Visual Words using stop words":
			imgList = getTop10SIFTWithoutStopWords(targetImg, app.allImages)
		
		targetImg.setMetricResult(imgList, metric=mode)
	
	app.updateImgList(mode, imgList)

if __name__ == '__main__':
	root = Tk()
	size = 800, 1280

	app = Example(root)
	metaData = readMetaData("./clothing_metadata.csv")
	app.setAllImages([customizedImage(img, Image.open("./dataset/"+img), metaData[img[:-4]]) for img in os.listdir("./dataset") if ".jpg" in img])
	root.geometry("1280x800")
	root.mainloop()
	app.cleanUp()

  
