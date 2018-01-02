"""
Author : 106753027 Jung, Liang@NCCUCS
Environment:
	OS : MacOS Sierra
	Python : 2.7.10
"""
from pylab import *
from Util import *

TITLE = ["Original", "After Mosaic"]

class Example(Frame):
  
	def __init__(self, parent):
		Frame.__init__(self, parent)   
		self.parent = parent
		self.initUI()
		self.currentImg = None

	def setAllImages(self, Images):
		self.allImages = Images

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
		self.mode = StringVar(self)
		self.mode.set("ColorHistogram")
		modeOm = OptionMenu(self, self.mode, "ColorHistogram", "ColorLayout").grid(row=1, column=1, pady=5, sticky=W)
		
		Label(self, text = "Block size: ", font=("Courier", 12, "bold")).grid(row=2, column=0, pady=5)
		self.blockSize = IntVar(self)
		self.blockSize.set(5)
		widthOm = OptionMenu(self, self.blockSize, *BLOCK_SIZE_LIST).grid(row=2, column=1, padx=5, pady=5, sticky=W)

		Button(self, text = "Mosiac!", command = lambda: startMosaic(self, self.currentImg, self.allImages, self.mode.get(), self.blockSize.get())).grid(row=3, column=1, pady=5)
		
		for col in xrange(2):
			titleLbl = Label(self, text=TITLE[col], font=("Courier", 12, "bold")).grid(row=4, column=col, padx=50)
		
		self.imgContainer = {"Original":Label(self), "Mosaic":Label(self)}
		self.imgContainer["Original"].grid(row=5, column=0, padx=5, pady=5)
		self.imgContainer["Mosaic"].grid(row=5, column=1, padx=5, pady=5)

def startMosaic(app, originalImg, imgDataset, mode, blockSize):
	if originalImg is None or imgDataset is None or 0 == len(imgDataset):
		print "Something goes wrong...images should not be None!"
		return
	
	width, height = originalImg.size
	blockWidth = width/blockSize
	blockHeight = height/blockSize

	imgBlocks = splitImageToBlocks(originalImg, blockSize)
	
	mosaicImg = Image.new("RGB", originalImg.size)
	
	width, height = originalImg.size

	for row in xrange(blockSize):
		for col in xrange(blockSize):
			mosaicImg.paste(searchBestCandidate(imgBlocks[row][col], imgDataset, mode, blockSize), (col*blockWidth, row*blockHeight))

	mosaicImg.show()
	
	tkImg = ImageTk.PhotoImage(mosaicImg, Image.ANTIALIAS)
	app.imgContainer["Mosaic"].configure(image=tkImg)
	app.imgContainer["Mosaic"].image = tkImg
	
if __name__ == '__main__':
	root = Tk()
	size = 960, 1280

	app = Example(root)
	app.setAllImages([ImageWithCache(Image.open("./dataset/"+imgName)) for imgName in os.listdir("./dataset") if ".jpg" in imgName])
	root.geometry("1280x960")
	root.mainloop()
	app.cleanUp()
