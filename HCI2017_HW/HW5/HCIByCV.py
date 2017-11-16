import cv2
import numpy as np

Cam = cv2.VideoCapture(0)

if None == Cam:
	print("No cam")
	exit()

while(True):
	Ret, Frame = Cam.read()
	cv2.imshow("Frame", cv2.flip(Frame, 1))
	
	Key = cv2.waitKey(30) & 0xff 
	if Key == ord('q'):
		break

Cam.release()
cv2.destroyAllWindows()
