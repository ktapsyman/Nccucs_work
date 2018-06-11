import os

import cv2
import numpy as np

from image_augmentor import ImageAugmentor

Augmentor = ImageAugmentor()

Images = Augmentor.get_random_transform(Images)
