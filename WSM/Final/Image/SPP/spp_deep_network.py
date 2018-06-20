import keras
import keras.backend as K
from keras.engine.topology import Layer
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D
from keras.applications.densenet import DenseNet121
from keras.applications.vgg16 import VGG16
import cv2
import csv
import numpy as np

CUSTOM_OUTPUT_CATEGORIES = 2
KStr = keras.backend.backend()
if KStr == 'tensorflow':
	keras.backend.set_image_dim_ordering('tf')

class SpatialPyramidPooling(Layer):
	'''Spatial pyramid pooling layer for 2D inputs.
	See Spatial Pyramid Pooling in Deep Convolutional Networks for Visual Recognition,
	K. He, X. Zhang, S. Ren, J. Sun
	# Arguments
		pool_list: list of int
			List of pooling regions to use. The length of the list is the number of pooling regions,
			each int in the list is the number of regions in that pool. For example [1,2,4] would be 3
			regions with 1, 2x2 and 4x4 max pools, so 21 outputs per feature map
	# Input shape
		4D tensor with shape:
		`(samples, channels, rows, cols)` if dim_ordering='th'
		or 4D tensor with shape:
		`(samples, rows, cols, channels)` if dim_ordering='tf'.
	# Output shape
		2D tensor with shape:
		`(samples, channels * sum([i * i for i in pool_list])`
	'''

	def __init__(self, pool_list, **kwargs):

		self.dim_ordering = K.image_dim_ordering()
		assert self.dim_ordering in {'tf', 'th'}, 'dim_ordering must be in {tf, th}'

		self.pool_list = pool_list

		self.num_outputs_per_channel = sum([i * i for i in pool_list])

		super(SpatialPyramidPooling, self).__init__(**kwargs)

	def build(self, input_shape):
		if self.dim_ordering == 'th':
			self.nb_channels = input_shape[1]
		elif self.dim_ordering == 'tf':
			self.nb_channels = input_shape[3]
	"""
	def get_output_shape_for(self, input_shape):
		return (input_shape[0], self.nb_channels * self.num_outputs_per_channel)
	"""
	def compute_output_shape(self, input_shape):
		return (input_shape[0], self.nb_channels * self.num_outputs_per_channel)

	def get_config(self):
		config = {'pool_list': self.pool_list}
		base_config = super(SpatialPyramidPooling, self).get_config()
		return dict(list(base_config.items()) + list(config.items()))

	def call(self, x, mask=None):

		input_shape = K.shape(x)

		if self.dim_ordering == 'th':
			num_rows = input_shape[2]
			num_cols = input_shape[3]
		elif self.dim_ordering == 'tf':
			num_rows = input_shape[1]
			num_cols = input_shape[2]

		row_length = [K.cast(num_rows, 'float32') / i for i in self.pool_list]
		col_length = [K.cast(num_cols, 'float32') / i for i in self.pool_list]

		outputs = []

		if self.dim_ordering == 'th':
			for pool_num, num_pool_regions in enumerate(self.pool_list):
				for jy in range(num_pool_regions):
					for ix in range(num_pool_regions):
						x1 = ix * col_length[pool_num]
						x2 = ix * col_length[pool_num] + col_length[pool_num]
						y1 = jy * row_length[pool_num]
						y2 = jy * row_length[pool_num] + row_length[pool_num]

						x1 = K.cast(K.round(x1), 'int32')
						x2 = K.cast(K.round(x2), 'int32')
						y1 = K.cast(K.round(y1), 'int32')
						y2 = K.cast(K.round(y2), 'int32')
						new_shape = [input_shape[0], input_shape[1],
									 y2 - y1, x2 - x1]
						x_crop = x[:, :, y1:y2, x1:x2]
						xm = K.reshape(x_crop, new_shape)
						pooled_val = K.max(xm, axis=(2, 3))
						outputs.append(pooled_val)

		elif self.dim_ordering == 'tf':
			for pool_num, num_pool_regions in enumerate(self.pool_list):
				for jy in range(num_pool_regions):
					for ix in range(num_pool_regions):
						x1 = ix * col_length[pool_num]
						x2 = ix * col_length[pool_num] + col_length[pool_num]
						y1 = jy * row_length[pool_num]
						y2 = jy * row_length[pool_num] + row_length[pool_num]

						x1 = K.cast(K.round(x1), 'int32')
						x2 = K.cast(K.round(x2), 'int32')
						y1 = K.cast(K.round(y1), 'int32')
						y2 = K.cast(K.round(y2), 'int32')

						new_shape = [input_shape[0], y2 - y1,
									 x2 - x1, input_shape[3]]

						x_crop = x[:, y1:y2, x1:x2, :]
						xm = K.reshape(x_crop, new_shape)
						pooled_val = K.max(xm, axis=(1, 2))
						outputs.append(pooled_val)

		if self.dim_ordering == 'th':
			outputs = K.concatenate(outputs)
		elif self.dim_ordering == 'tf':
			# outputs = K.concatenate(outputs,axis = 1)
			outputs = K.concatenate(outputs)
			# outputs = K.reshape(outputs,(len(self.pool_list),self.num_outputs_per_channel,input_shape[0],input_shape[1]))
			# outputs = K.permute_dimensions(outputs,(3,1,0,2))
			# outputs = K.reshape(outputs,(input_shape[0], self.num_outputs_per_channel * self.nb_channels))

		return outputs

def Spp():
	
	# uses theano ordering. Note that we leave the image size as None to allow multiple image sizes
	model = Sequential()

	model.add(Conv2D(96, (11, 11), padding='same', input_shape=(None, None, 3), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Conv2D(32, (3, 3), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Conv2D(64, (3, 3), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(SpatialPyramidPooling([1, 2, 4]))

	model.add(Dense(4096, activation='relu', name='dense_1'))
	model.add(Dropout(0.5))
	model.add(Dense(4096, activation='relu', name='dense_2'))
	model.add(Dropout(0.5))
	model.add(Dense(CUSTOM_OUTPUT_CATEGORIES, name='dense_3'))
	model.add(Activation('softmax'))
	return model

def ReadLabels(FullPath):
	Ret = []
	with open(FullPath, "r") as LabelFile:
		Reader = csv.reader(LabelFile, delimiter=' ')
		for Col in Reader:
			Ret.append([Col[1], float(Col[2])])
	return Ret

def LoadData():
	BaseDirPath = "./databaserelease2/"
	ImgDirList = ["fastfading", "gblur", "jp2k", "jpeg", "wn"]
	TrainingX = []
	TrainingY = []
	for Dir in ImgDirList:
		for LabelTuple in ReadLabels(BaseDirPath+Dir+"/info.txt"):
			ImgPath = BaseDirPath+Dir+"/" + LabelTuple[0]
			TrainingX.append(cv2.resize(cv2.imread(ImgPath, cv2.IMREAD_COLOR), (224,224)))
			TrainingY.append(LabelTuple[1])
	return np.array(TrainingX), np.array(TrainingY)

def Main():
	TrainingX, TrainingY = LoadData()
	TrainingY = TrainingY.reshape((-1, 1))
	print(len(TrainingX))
	ValidX = TrainingX[800:]
	TrainingX = TrainingX[:800]
	ValidY = TrainingY[800:]
	TrainingY = TrainingY[:800]
	print(TrainingX.shape)
	print(TrainingY.shape)
	
	"""
	model = Spp()
	"""
	model = Sequential()
	model.add(DenseNet121(include_top=False, weights='imagenet', input_shape=(224, 224, 3)))
	model.add(Flatten())
	model.add(Dense(256, activation='relu'))
	model.add(Dense(1, activation='sigmoid'))

	model.compile(loss='mean_squared_error', optimizer='ADAM')
	model.fit(x=TrainingX, y=TrainingY, batch_size=64, epochs=100, verbose=1, validation_data=(ValidX, ValidY))
	

Main()
