#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author : 106753027 Jung, Liang@NCCUCS
Environment:
	OS : MacOS Sierra
	Python : 2.7.10
	numpy : 1.8.0rc1
	pyaudio : 0.2.11
	scipy : 0.13.0b1
'''

import wave
import matplotlib.pylab as pl
import numpy as np
import pyaudio  
import scipy

from Tkinter import *
import tkFileDialog 


def wave_plot(wave_data, time):
	pl.subplot(211) 
	pl.plot(time, wave_data[0])
	pl.subplot(212) 
	pl.plot(time, wave_data[1], c="g")
	pl.xlabel("time (seconds)")
	pl.show()


def wave_open(filename):
	# 打開WAV文檔
	f = wave.open(filename, "rb")

	# 讀取格式信息
	params = f.getparams()
	nchannels, sampwidth, framerate, nframes = params[:4]

	# 讀取波形數據
	str_data = f.readframes(nframes)
	f.close()

	#將波形數據轉換為數組
	wave_data = np.fromstring(str_data, dtype=np.short)
	wave_data.shape = -1, 2
	wave_data = wave_data.T
	time = np.arange(0, nframes) * (1.0 / framerate)
	
	return wave_data, time, list(params)


def wave_write(wave_data, filename, params):
	#將數組轉換回波形數據
	wave_data = wave_data.T
	wave_data.shape = -1, 2
	wave_data = wave_data.astype(np.short)
	
	f = wave.open(filename, "wb")
	# 配置聲道數、量化位數和取樣頻率
	f.setparams(params)
	# 將wav_data轉換為二進制數據寫入文件
	f.writeframes(wave_data.tostring())
	f.close()


def play_file(filename):
	#define stream chunk   
	chunk = 1024  
	print "play_file ",filename
	#open a wav format music  
	f = wave.open(filename,"rb")  
	#instantiate PyAudio  
	p = pyaudio.PyAudio()  
	#open stream  
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
					channels = f.getnchannels(),  
					rate = f.getframerate(),  
					output = True)  
	#read data  
	data = f.readframes(chunk)  
	
	#paly stream  
	while data != '':  
		stream.write(data)  
		data = f.readframes(chunk)  
	
	#stop stream  
	stream.stop_stream()  
	stream.close()  
	f.close()
	
	#close PyAudio  
	p.terminate()  

# # Q1. 振福

def Q1(WAVE_NOW_FILENAME):
	wave_data, time, params = wave_open(WAVE_NOW_FILENAME)
	wave_plot(wave_data, time)
	wave_data = np.array([sample * 3 for sample in wave_data])
	wave_plot(wave_data, time)
	wave_write(wave_data, "Q1.wav", params)

# # Q2.頻率


def Q2(WAVE_NOW_FILENAME):
	wave_data, time, params = wave_open(WAVE_NOW_FILENAME)
	params = (params[0], params[1], params[2]*2, params[3], params[4], params[5])
	wave_write(wave_data, "Q2.wav", params)


# Q3.FFT

def tune_block(data, freq_muliplier):
	data_from_fft = np.fft.fft(data)
	new_data = [data_from_fft[round(i/freq_muliplier)] for i in xrange(len(data_from_fft))]
	return np.fft.ifft(new_data)

def Tune(data, framerate, freq_muliplier):
	ret = []
	chunk_size = framerate/8
	for i in xrange(0, len(data), chunk_size):
		chunk = data[i:i+chunk_size]
		ret += list(tune_block(chunk, freq_muliplier))
	return ret

def Q3(WAVE_NOW_FILENAME):
	wave_data, time, params = wave_open(WAVE_NOW_FILENAME)
	for channel in xrange(len(wave_data)):
		wave_data[channel] = Tune(wave_data[channel], params[2], 2)

	wave_write(wave_data, "Q3.wav", params)

# Q4.回音


def Q4(WAVE_NOW_FILENAME):
	wave_data, time, params = wave_open(WAVE_NOW_FILENAME)
	for channel in xrange(len(wave_data)):
		for i in xrange(10000, len(wave_data[channel])):
			wave_data[channel][i] += wave_data[channel][i-10000]*0.6

	wave_write(wave_data, "Q4.wav", params)




# Q5.自由發揮


def Q5(WAVE_NOW_FILENAME):
	wave_data, time, params = wave_open(WAVE_NOW_FILENAME)
	for channel in xrange(len(wave_data)):
		percentage = 1.0/float(len(wave_data[channel]))
		volume = 1.0
		for i in xrange(0, len(wave_data[channel])):
			volume -= percentage
			wave_data[channel][i] = wave_data[channel][i]*volume

	wave_write(wave_data, "Q5.wav", params)


# Gui

	 
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"
WAVE_NOW_FILENAME = ""

audio = pyaudio.PyAudio()


class GUIDemo(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()
		self.createWidgets()
 
	def createWidgets(self):
		self.load = Button(self)
		self.load["text"] = "Load"
		self.load.grid(row=2, column=1)
		self.load["command"] =  self.loadMethod
		self.q1 = Button(self)
		self.q1["text"] = "Q1-Volume"
		self.q1.grid(row=2, column=2)
		self.q1["command"] =  self.q1Method
		self.q2 = Button(self)
		self.q2["text"] = "Q2-Pitch"
		self.q2.grid(row=2, column=3)
		self.q2["command"] =  self.q2Method
		self.q3 = Button(self)
		self.q3["text"] = "Q3-FFT"
		self.q3.grid(row=2, column=4)
		self.q3["command"] =  self.q3Method
		self.q4 = Button(self)
		self.q4["text"] = "Q4-Echo"
		self.q4.grid(row=2, column=5)
		self.q4["command"] =  self.q4Method
		self.q5 = Button(self)
		self.q5["text"] = "Q5-Fadeout Effect"
		self.q5.grid(row=2, column=6)
		self.q5["command"] =  self.q5Method
		self.play = Button(self)
		self.play["text"] = "Play"
		self.play.grid(row=2, column=7)
		self.play["command"] =  self.playMethod
 
		self.displayText = Label(self)
		self.displayText["text"] = "Load a wav file first!"
		self.displayText.grid(row=3, column=0, columnspan=7)
 
	def loadMethod(self):
		self.displayText["text"] = "Load button clicked"

		ftypes = [('Python files', '*.py'), ('Wave files','*.wav'), ('All files', '*')]
		dlg = tkFileDialog.Open(self, filetypes = ftypes)
		fl = dlg.show()
		global WAVE_NOW_FILENAME
		
		if fl != '':
			WAVE_NOW_FILENAME = fl
			print "load ",WAVE_NOW_FILENAME
			wave_data, time, params = wave_open(fl)
			# wave_plot(wave_data, time)
		return WAVE_NOW_FILENAME
			

	def q1Method(self):
		if None == WAVE_NOW_FILENAME or 0 >= len(WAVE_NOW_FILENAME):
			self.displayText["text"] = "File not loaded yet!"
			return
		self.displayText["text"] = "Volume button clicked"
		Q1(WAVE_NOW_FILENAME)
 
	def q2Method(self):
		if None == WAVE_NOW_FILENAME or 0 >= len(WAVE_NOW_FILENAME):
			self.displayText["text"] = "File not loaded yet!"
			return
		self.displayText["text"] = "Pitch button clicked"
		Q2(WAVE_NOW_FILENAME)
 
	def q3Method(self):
		if None == WAVE_NOW_FILENAME or 0 >= len(WAVE_NOW_FILENAME):
			self.displayText["text"] = "File not loaded yet!"
			return
		self.displayText["text"] = "FFT button clicked"
		Q3(WAVE_NOW_FILENAME)

	def q4Method(self):
		if None == WAVE_NOW_FILENAME or 0 >= len(WAVE_NOW_FILENAME):
			self.displayText["text"] = "File not loaded yet!"
			return
		self.displayText["text"] = "Echo button clicked"
		Q4(WAVE_NOW_FILENAME)

	def q5Method(self):
		self.displayText["text"] = "Fadeout Effect button clicked"
		Q5(WAVE_NOW_FILENAME)
		
	def playMethod(self):
		if None == WAVE_NOW_FILENAME or 0 >= len(WAVE_NOW_FILENAME):
			self.displayText["text"] = "File not loaded yet!"
			return
		self.displayText["text"] = "Playing : " + WAVE_NOW_FILENAME
		play_file(WAVE_NOW_FILENAME)


if __name__ == '__main__':
	root = Tk()
	app = GUIDemo(master=root)
	app.mainloop()




