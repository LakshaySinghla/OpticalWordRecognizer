#This program is used for giving custom user input to the NN and see the output.

import get_equivalent_letter 
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
import numpy as np
import cv2
from matplotlib import pyplot as plt



def image_for_extraction(raw_image):
	raw_image = cv2.GaussianBlur(raw_image,(3,3),0)
	ret,no_sm_bw_image = cv2.threshold(raw_image,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	return no_sm_bw_image

# import mnist_loader
# training_data, validation_data, test_data = mnist_loader.load_data_wrapper()

# import NeuralNetwork.my_network
# from NeuralNetwork import my_network
# import numpy as np
# from functools import partial
# from nn_two_stage.second_nn import get_let_from_2nd_nn_ijltIL1
# from nn_two_stage.second_nn import get_let_from_2nd_nn_ceg

def get_string_from_nn(all_letters):
	# net = my_network.Network([1024, 30, 66], cost=my_network.CrossEntropyCost)
	
	# np_load_old = partial(np.load)
	# # modify the default parameters of np.load
	# np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)
	# biases_saved = np.load('NeuralNetwork/biases.npy')
	# weights_saved = np.load('NeuralNetwork/weights.npy')
	# np.load = np_load_old

	model = load_model("NewNeuralNet.h5")
	# score = model.evaluate(x_test, y_test)
	# print("%s: %.2f%%" % (model.metrics_names[1], score[1]*100))

	word_string = ""
	i = 0
	for x in all_letters:

		# output = np.argmax(net.feedforward(x, biases_saved = biases_saved, weights_saved = weights_saved))
		# #second stage classification below
		# if (output in (18, 19, 21, 29, 44, 47, 1)):
		# 	output = get_let_from_2nd_nn_ijltIL1(x)
		# elif (output in (12, 14, 42)):
		# 	output = get_let_from_2nd_nn_ceg(x)
		
		
		# y = x.reshape(32,32,1)
		# y = y/255
		# plt.imshow(y, interpolation='nearest')
		# plt.show()

		x = x.reshape(32,32)
		x = image_for_extraction(x)
		# x = cv2.resize(x, (64,64))
		# cv2.imshow("Img",x)
		# cv2.waitKey()
		x = x.reshape(1,1,32,32)
		output = np.argmax(model.predict(x))
		# print("x.size ", x.shape, " Output ", output)
		
		# word_string = word_string + "a"
		word_string = word_string + get_equivalent_letter.mapping[output]
		i = i + 1
	return word_string