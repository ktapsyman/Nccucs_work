import cv2
import numpy as np
import sys

Img1 = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
Img2 = cv2.imread(sys.argv[2], cv2.IMREAD_GRAYSCALE)



ResizedImg1 = cv2.resize(Img1, (128, 128))
ResizedImg2 = cv2.resize(Img2, (128, 128))

cv2.imshow("Img1", ResizedImg1)
cv2.imshow("Img2", ResizedImg2)

print(np.linalg.norm(ResizedImg1.flatten() - ResizedImg2.flatten()))

cv2.waitKey()
cv2.destroyAllWindows()
