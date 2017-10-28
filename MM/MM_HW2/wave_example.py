#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wave_hw2 import *

wave_data, time, params = wave_open("file.wav")
wave_plot(wave_data, time)


print "nchannels: ", params[0]
print "sampwidth: ", params[1]
print "framerate: ", params[2]
print "nframes: ", params[3]
