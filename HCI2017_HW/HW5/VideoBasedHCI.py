import cv2
import numpy as np
import threading
from threading import Timer


ColorRed = (0, 0, 108)
ColorAoi = (255, 108, 0)

BtnNextROI = ((980, 420), (1280, 720))
BtnPrevROI = ((0, 420), (300, 720))

BtnPrevBase = 0
BtnNextBase = 0

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

def CheckROIEntered(BtnName, CurrentFrame, Base):
	if 0 == Base:
		if BtnName == "Prev":
			global BtnPrevBase
			BtnPrevBase = cv2.countNonZero(CurrentFrame)
		else:
			global BtnNextBase
			BtnNextBase = cv2.countNonZero(CurrentFrame)
		return False
	return cv2.countNonZero(CurrentFrame) - Base >= 3000


def OnClick(BtnName):
	global CurrentImgIndex
	if BtnName == "Prev":
		CurrentImgIndex = (CurrentImgIndex-1)
		if CurrentImgIndex <= 0:
			CurrentImgIndex = CurrentImgIndex%3+1
	elif BtnName == "Next":
		CurrentImgIndex = (CurrentImgIndex+1)
		if CurrentImgIndex >= 4:
			CurrentImgIndex = CurrentImgIndex%3
	Img = cv2.imread("./Imgs/Img" + str(CurrentImgIndex) + ".jpg")
	cv2.imshow("Img", Img)

	CountingDown = False

def GUIThread():
	Camera = InitializeCam()
	Background = None
	CountingDown = False
	ClickTimer = None
	LastDiff = None
	while (True):
		Ret, Frame = Camera.read()
		CurrentFrame = cv2.flip(Frame, 1)

		DrawROI(CurrentFrame, BtnPrevROI, ColorAoi, "Prev image")
		DrawROI(CurrentFrame, BtnNextROI, ColorAoi, "Next image")
		cv2.imshow("Frame", CurrentFrame)

		if Background is None:
			Background = CurrentFrame
		else:
			Diff = cv2.cvtColor(cv2.absdiff(Background, CurrentFrame), cv2.COLOR_BGR2GRAY)
			if CheckROIEntered("Prev", Diff[BtnPrevROI[0][1]:BtnPrevROI[1][1], BtnPrevROI[0][0]:BtnPrevROI[1][0]], BtnPrevBase):
				if CountingDown:
					continue
				CountingDown = True
				ClickTimer = Timer(2, OnClick, kwargs={'BtnName':"Prev"})
				ClickTimer.start()
				continue
			
			if CheckROIEntered("Next", Diff[BtnNextROI[0][1]:BtnNextROI[1][1], BtnNextROI[0][0]:BtnNextROI[1][0]], BtnNextBase):
				if CountingDown:
					continue
				CountingDown = True
				ClickTimer = Timer(2, OnClick, kwargs={'BtnName':"Next"})
				ClickTimer.start()
				continue
			
			if CountingDown:
				CountingDown = False
				if ClickTimer is not None:
					ClickTimer.cancel()

		if cv2.waitKey(100) &0xff == ord('q'):
			break

	Camera.release()
	cv2.destroyAllWindows()

MainThread = threading.Thread(target=GUIThread)
MainThread.start()
