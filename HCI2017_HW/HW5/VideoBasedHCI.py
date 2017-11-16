import cv2
import numpy as np
import threading
from threading import Timer
from time import sleep

ColorRed = (0, 0, 108)
ColorAoi = (255, 108, 0)

BtnNextROI = ((980, 420), (1280, 720))
BtnPrevROI = ((0, 420), (300, 720))

CurrentImgIndex = 0

def InitializeCam():
	Camera = cv2.VideoCapture(0)
	Camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
	Camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
	return Camera
	
def DrawROI(Img, RectPoints, Color, Text):
	cv2.rectangle(Img, RectPoints[0], RectPoints[1], Color, 5)
	cv2.putText(Img, Text, (RectPoints[0][0]+75, RectPoints[0][1]+75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
	return

def CheckROIEntered(CurrentFrame):
	return cv2.countNonZero(CurrentFrame) > 1000


def OnClick(BtnName):
	global CurrentImgIndex
	print("OnClick : " + BtnName)
	if BtnName == "Prev":
		CurrentImgIndex = (CurrentImgIndex-1)
		if CurrentImgIndex <= 0:
			CurrentImgIndex = CurrentImgIndex%3+1
	elif BtnName == "Next":
		CurrentImgIndex = (CurrentImgIndex+1)
		if CurrentImgIndex >= 4:
			CurrentImgIndex = CurrentImgIndex%3
	Img = cv2.imread("./Imgs/Img" + str(CurrentImgIndex) + ".jpg")
	Img = cv2.resize(Img, (200, 200))
	cv2.imshow("Img", Img)

Substractor = cv2.bgsegm.createBackgroundSubtractorMOG()

def GUIThread():
	Camera = InitializeCam()
	CountingDown = False
	ClickTimer = None
	LastDiff = None
	while (True):
		Ret, Frame = Camera.read()
		CurrentFrame = cv2.flip(Frame, 1)

		DrawROI(CurrentFrame, BtnPrevROI, ColorAoi, "Prev image")
		DrawROI(CurrentFrame, BtnNextROI, ColorAoi, "Next image")
		
		BgMask = Substractor.apply(CurrentFrame)
		cv2.imshow("Frame", CurrentFrame)
		
		if CheckROIEntered(BgMask[BtnNextROI[0][1]:BtnNextROI[1][1], BtnNextROI[0][0]:BtnNextROI[1][0]]):
			if CountingDown:
				sleep(0.033)
				continue
			CountingDown = True
			OnClick("Next")
			#ClickTimer = Timer(0, OnClick, kwargs={'BtnName':"Next"})
			#ClickTimer.start()
			
		elif CheckROIEntered(BgMask[BtnPrevROI[0][1]:BtnPrevROI[1][1], BtnPrevROI[0][0]:BtnPrevROI[1][0]]):
			if CountingDown:
				sleep(0.033)
				continue
			CountingDown = True
			OnClick("Prev")
			#ClickTimer = Timer(0, OnClick, kwargs={'BtnName':"Prev"})
			#ClickTimer.start()
		else:
			if CountingDown:
				CountingDown = False
				if ClickTimer is not None:
					ClickTimer.cancel()		

		if cv2.waitKey(30) &0xff == ord('q'):
			break

	Camera.release()
	cv2.destroyAllWindows()

GUIThread()
#MainThread = threading.Thread(target=GUIThread)
#MainThread.start()
