import tensorflow as tf
from keras.models import Sequential
from keras.layers import Embedding
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM, GRU
from keras.preprocessing.sequence import pad_sequences

from Utility import *

def CreateModel(InputSize, Data):
	Model = Sequential()
	Model.add(LSTM(InputSize, input_shape=(Data.shape[1], Data.shape[2])))
	Model.add(Dense(1))
	"""
	Model.add(GRU(256, activation='relu', recurrent_activation='relu',
		return_sequences = True))
	Model.add(Dropout(0.5))
	Model.add(GRU(256, activation='relu', recurrent_activation='relu'))
	Model.add(Dropout(0.5))
	Model.add(Dense(1, activation = 'sigmoid'))
	"""
	Model.compile(loss='mean_squared_error', optimizer='rmsprop')
	return Model

def SignatureVerifier():
	RealSignatures = ReadDataFromDir("./dataset/Real", "Real")
	FakeSignatures = ReadDataFromDir("./dataset/Fake", "Fake")

	TrainingData = RealSignatures+FakeSignatures
	
	TrainingX = np.array([Data[1] for Data in TrainingData])
		
	TrainingLabel = np.array([Data[0] for Data in TrainingData])
	TrainingX = pad_sequences(TrainingX)
	print(len(TrainingX))
	print (TrainingX.shape)
	Model = CreateModel(len(TrainingX), TrainingX)
	Model.fit(TrainingX, TrainingLabel)


SignatureVerifier()
