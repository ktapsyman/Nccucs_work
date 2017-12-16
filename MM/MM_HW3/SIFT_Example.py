#siftDescriptor!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
from numpy import array
import sift
from pylab import *


imname = './dataset/ukbench00883.jpg'

im1 = array(Image.open(imname).convert('L'))

sift.process_image(imname,'Test.sift')

l1,d1 = sift.read_features_from_file('Test.sift')
figure()
gray()
sift.plot_features(im1,l1,circle=True)
show()

