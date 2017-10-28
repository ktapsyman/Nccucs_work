#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wave
import pylab as pl
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


# # Q2.頻率


def Q2(WAVE_NOW_FILENAME):
    wave_data, time, params = wave_open(WAVE_NOW_FILENAME)


# Q3.FFT



def Q3(WAVE_NOW_FILENAME):
    wave_data, time, params = wave_open(WAVE_NOW_FILENAME)

# Q4.回音


def Q4(WAVE_NOW_FILENAME):
    wave_data, time, params = wave_open(WAVE_NOW_FILENAME)



# Q5.自由發揮


def Q5(WAVE_NOW_FILENAME):
    wave_data, time, params = wave_open(WAVE_NOW_FILENAME)


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
        self.record = Button(self)
        self.record["text"] = "Record"
        self.record.grid(row=2, column=0)
        self.record["command"] =  self.recordMethod
        self.load = Button(self)
        self.load["text"] = "Load"
        self.load.grid(row=2, column=1)
        self.load["command"] =  self.loadMethod
        self.q1 = Button(self)
        self.q1["text"] = "Volume"
        self.q1.grid(row=2, column=2)
        self.q1["command"] =  self.q1Method
        self.q2 = Button(self)
        self.q2["text"] = "Pitch"
        self.q2.grid(row=2, column=3)
        self.q2["command"] =  self.q2Method
        self.q3 = Button(self)
        self.q3["text"] = "FFT"
        self.q3.grid(row=2, column=4)
        self.q3["command"] =  self.q3Method
        self.q4 = Button(self)
        self.q4["text"] = "Echo"
        self.q4.grid(row=2, column=5)
        self.q4["command"] =  self.q4Method
        self.q5 = Button(self)
        self.q5["text"] = "Reverse"
        self.q5.grid(row=2, column=6)
        self.q5["command"] =  self.q5Method
        self.play = Button(self)
        self.play["text"] = "Play"
        self.play.grid(row=2, column=7)
        self.play["command"] =  self.playMethod
 
        self.displayText = Label(self)
        self.displayText["text"] = "something happened"
        self.displayText.grid(row=3, column=0, columnspan=7)
     
    def recordMethod(self):	 
        self.displayText["text"] = "This is Record button." 
        global WAVE_NOW_FILENAME

        # start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        print "recording..."
        frames = []
         
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print "finished recording"
         
         
        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        WAVE_NOW_FILENAME = WAVE_OUTPUT_FILENAME
         
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

 
    def loadMethod(self):
        self.displayText["text"] = "This is Load button."

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
        self.displayText["text"] = "This is Volume button."
        Q1(WAVE_NOW_FILENAME)
 
    def q2Method(self):
        self.displayText["text"] = "This is Pitch button."
        Q2(WAVE_NOW_FILENAME)
 
    def q3Method(self):
        self.displayText["text"] = "This is FFT button."
        Q3(WAVE_NOW_FILENAME)

    def q4Method(self):
        self.displayText["text"] = "This is Echo button."
        Q4(WAVE_NOW_FILENAME)

    def q5Method(self):
        self.displayText["text"] = "This is Reverse button."
        Q5(WAVE_NOW_FILENAME)
        
    def playMethod(self):
        self.displayText["text"] = "This is Play button."
        play_file(WAVE_NOW_FILENAME)


if __name__ == '__main__':

    root = Tk()
    app = GUIDemo(master=root)
    app.mainloop()




