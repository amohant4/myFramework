"""
Created on Tue May 07 09:55:20 2018
@Author: Abinash Mohanty
"""

import _init_paths
import networks
import emulator as em
import numpy as np
import cPickle 

import cv2
from matplotlib import pyplot as plt

if __name__ == "__main__":

	# Read image and convert to batch of size 1 (Emulator supports batch processing)
	img = cv2.imread('../data/3.jpg')
	sh = img.shape
	img = np.reshape(img, (1, sh[0], sh[1], sh[2]))

	plt.imshow(cv2.cvtColor(img[0,...],cv2.COLOR_BGR2RGB)), plt.title('original')
	plt.show()	

	# Get the network you want from the factory. isHardware has to be True
	net = networks.factory.get_network(name='testNet', isHardware=True)

	# Create a feed dictionary for the image to pass it as an input to NN
	feed_dict={net.img:img}

	# Demo to show how to load model values
	weight = np.zeros((3,3,3,3))
	for o in range(3):
		for i in range(3):
			for h in range(3):
				for w in range(3):
					if (w == 1) or (h == 1) :
						weight[o,i,h,w] = 1.0
					else:
						weight[o,i,h,w] = -1.0
	ww = em.get_variable('convv2/weights')		
	ww.load(weight)	
	ww = em.get_variable('convv1/weights')		
	ww.load(weight)	

	# To get any output we need to create a Session object
	sess = em.Session()

	#  Call the run function with the net.get_output(_layer_name_) and feed dict as input 
	result = sess.run(net.get_output('poolingTest'), feed_dict=feed_dict)
	result = np.uint8(result)

	plt.imshow(cv2.cvtColor(result[0,...],cv2.COLOR_BGR2RGB)), plt.title('fromNet')
	plt.show()

	result1 = sess.run(net.get_output('convv2'), feed_dict=feed_dict)
	result1 = np.uint8(result1)

	plt.imshow(cv2.cvtColor(result1[0,...],cv2.COLOR_BGR2RGB)), plt.title('fromNet')
	plt.show()	
