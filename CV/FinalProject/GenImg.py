import os
import sys
import cv2
from keras.preprocessing import image

DATASET_PATH=sys.argv[1]

ImgGenerator = image.ImageDataGenerator(rotation_range=15, width_shift_range=5, height_shift_range=5)

for Text in os.listdir(DATASET_PATH):
	if len(Text) > 1:
		print(Text[1])
	os.system("cp -a " + DATASET_PATH+"/"+Text + " ./Tmp/")
	if not os.path.exists("./Augmented/"+Text):
		os.system("mkdir ./Augmented/"+Text)

	Flow = ImgGenerator.flow_from_directory("./Tmp/", batch_size=1, shuffle=False, save_to_dir="./Augmented/"+Text, save_prefix="gen", save_format="jpg", target_size=(128, 128))
	
	CurrentDataCount = len([File for File in os.listdir(DATASET_PATH+"/"+Text) if "jpg" in File])
	Residual = 20 - CurrentDataCount
	
	for Gen in Flow:
		if 0 == Residual:
			break
		Residual -= 1

	if os.path.exists("./Tmp/"+Text):
		os.system("rm -r ./Tmp/" + Text)
"""
Flow = ImgGenerator.flow_from_directory("./TestImg/", batch_size=1, shuffle=False, save_to_dir="./Augmented/", save_prefix="gen", target_size=(128, 128))
for Id in range(len(Flow)):
	print(Flow.next()[1])
"""
#cv2.waitKey()
#cv2.destroyAllWindows()
