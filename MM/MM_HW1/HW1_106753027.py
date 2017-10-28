'''
Author : 106753027 Jung, Liang@NCCUCS
Environment:
	OS : MacOS Sierra
	Python : 2.7.10
	Numpy : 1.8.0rc1
'''

from PIL import Image

PENGUINS_FILENAME = "Penguins.jpg"
PENGUINS_NOISE_FILENAME = "Penguins_noise.jpg"
CHRYSANTHEMUM_FILENAME = "Chrysanthemum.jpg"
ELSA_FILENAME = "Elsa.jpg"

def RGBToGrayScaleStandard(RGBTuple):
	if type(RGBTuple) is not tuple:
		raise TypeError("Input must be RGB tuple!")
	return int((RGBTuple[0]+RGBTuple[1]+RGBTuple[2])/3)

def RGBToGrayScalePsychological(RGBTuple):
	if type(RGBTuple) is not tuple:
		raise TypeError("Input must be RGB tuple!")
	return int(0.587*RGBTuple[0] + 0.299*RGBTuple[1] + 0.114*RGBTuple[2])

def Q1(Img):
	Pixels = Img.load()
	Width, Height = Img.size
	Boundary = int(Width/3)
	Multiplier = 1
	for X in xrange(Width):
		for Y in xrange(Height):
			if X > Boundary:
				Multiplier += 1
				Boundary += int(Width/3)
				continue
			Pixel = Pixels[X, Y]
			if Multiplier == 1:
				Pixels[X, Y] = (Pixel[0]*3, Pixel[1], Pixel[2])

			elif Multiplier == 2:
				Pixels[X, Y] = (Pixel[0], Pixel[1]*3, Pixel[2])
				
			else:
				Pixels[X, Y] = (Pixel[0], Pixel[1], Pixel[2]*3)
	Img.save("Q1.jpg")
	return

def Q2(Img):
	Pixels = Img.load()
	Width, Height = Img.size
	Boundary = int(Width/4)
	Multiplier = 1
	for X in xrange(Width):
		for Y in xrange(Height):
			if X > Boundary:
				Multiplier += 1
				Boundary += int(Width/4)
				continue
			Pixel = Pixels[X, Y]
			if Multiplier == 1:
				Pixels[X, Y] = (Pixel[0]*3, Pixel[1], Pixel[2], Pixel[3])

			elif Multiplier == 2:
				Pixels[X, Y] = (Pixel[0], Pixel[1]*3, Pixel[2], Pixel[3])
			
			elif Multiplier == 3:
				Pixels[X, Y] = (Pixel[0], Pixel[1], Pixel[2]*3, Pixel[3])
				
			else:
				Pixels[X, Y] = (Pixel[0], Pixel[1], Pixel[2], Pixel[3]*3)
	Img.save("Q2.jpg")
	return

def Q3(Img):
	Pixels = Img.load()
	Width, Height = Img.size
	for X in xrange(Width):
		for Y in xrange(Height):
			Pixel = Pixels[X, Y]
			Pixels[X, Y] = (255 - Pixel[0], 255 - Pixel[1], 255 - Pixel[2])
	Img.save("Q3.jpg")
	return

def Q4(Img):
	Pixels = Img.load()
	Width, Height = Img.size
	X = 0
	Y = 0
	while X < Width:
		while Y < Height:
			BasePixel = Pixels[X, Y]
			for BlockX in range(8):
				for BlockY in range(8):
					Pixels[X + BlockX, Y + BlockY] = BasePixel
			Y += 8
		X += 8	
		Y = 0
	Img.save("Q4.jpg")
	return

def Q5(Img):
	Width, Height = Img.size
	ImgForStandardGrayScale = Img.copy()
	PixelsForStandard = ImgForStandardGrayScale.load()

	ImgForPsychologicalGrayScale = Img.copy()
	PixelsForPsychological = ImgForPsychologicalGrayScale.load()

	for X in xrange(Width):
		for Y in xrange(Height):
			GrayScaleStandard = RGBToGrayScaleStandard(PixelsForStandard[X, Y])
			PixelsForStandard[X, Y] = GrayScaleStandard, GrayScaleStandard, GrayScaleStandard

			GrayScalePsychological =  RGBToGrayScalePsychological(PixelsForPsychological[X, Y])
			PixelsForPsychological[X, Y] = GrayScalePsychological, GrayScalePsychological, GrayScalePsychological

	ImgForStandardGrayScale.save("Q5-1.jpg")
	ImgForPsychologicalGrayScale.save("Q5-2.jpg")
	return

def Q6(Img):
	Width, Height = Img.size

	BlackWhiteThreshold20 = Img.copy()
	BlackWhiteThreshold64 = Img.copy()
	BlackWhiteThreshold180 = Img.copy()
	
	Threshold20Pixels = BlackWhiteThreshold20.load()
	Threshold64Pixels = BlackWhiteThreshold64.load()
	Threshold180Pixels = BlackWhiteThreshold180.load()

	for X in xrange(Width):
		for Y in xrange(Height):
			GrayScale = RGBToGrayScaleStandard(Threshold20Pixels[X, Y])
			Threshold20Pixels[X, Y] = (0, 0, 0) if GrayScale < 20 else (255, 255, 255)
			Threshold64Pixels[X, Y] = (0, 0, 0) if GrayScale < 64 else (255, 255, 255)
			Threshold180Pixels[X, Y] = (0, 0, 0) if GrayScale < 180 else (255, 255, 255)
	
	BlackWhiteThreshold20.save("Q6-1.jpg")
	BlackWhiteThreshold64.save("Q6-2.jpg")
	BlackWhiteThreshold180.save("Q6-3.jpg")
	return

def Q7(Img):
	Width, Height = Img.size
	
	RBG = Img.copy()
	GRB = Img.copy()
	GBR = Img.copy()
	BRG = Img.copy()
	BGR = Img.copy()
	
	RBGPixels = RBG.load()
	GRBPixels = GRB.load()
	GBRPixels = GBR.load()
	BRGPixels = BRG.load()
	BGRPixels = BGR.load()
	
	for X in xrange(Width):
		for Y in xrange(Height):
			RBGPixels[X, Y] = (RBGPixels[X, Y][0], RBGPixels[X, Y][2], RBGPixels[X, Y][1])
			GRBPixels[X, Y] = (GRBPixels[X, Y][1], GRBPixels[X, Y][0], GRBPixels[X, Y][2])
			GBRPixels[X, Y] = (GBRPixels[X, Y][1], GBRPixels[X, Y][2], GBRPixels[X, Y][0])
			BRGPixels[X, Y] = (BRGPixels[X, Y][2], BRGPixels[X, Y][0], BRGPixels[X, Y][1])
			BGRPixels[X, Y] = (BGRPixels[X, Y][2], BGRPixels[X, Y][1], BGRPixels[X, Y][0])

	RBG.save("Q7-1.jpg")
	GRB.save("Q7-2.jpg")
	GBR.save("Q7-3.jpg")
	BRG.save("Q7-4.jpg")
	BGR.save("Q7-5.jpg")

	return

def Q8(Img):
	return

def Q9(Img):
	return

def Q10(Img):
	return

def Q11(Img):
	return

def Q12(Elsa, Flower):
	return

with Image.open(PENGUINS_FILENAME) as PenguinImg, Image.open(PENGUINS_NOISE_FILENAME) as PenguinNoisedImg, Image.open(ELSA_FILENAME) as ElsaImg, Image.open(CHRYSANTHEMUM_FILENAME) as FlowerImg:
	PenguinImg.load()
	PenguinNoisedImg.load()
	ElsaImg.load()
	FlowerImg.load()
	#Q1(PenguinImg.copy())
	#Q2(PenguinImg.copy().convert("CMYK"))
	#Q3(PenguinImg.copy())
	#Q4(PenguinImg.copy())
	#Q5(PenguinImg)
	#Q6(PenguinImg)
	Q7(PenguinImg)
	Q8(PenguinImg.copy())
	Q9(PenguinImg.copy())
	Q10(PenguinNoisedImg)
	Q11(PenguinImg.copy())
	Q12(ElsaImg, FlowerImg)

