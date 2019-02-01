"""
Created on Tue May 02 15:34:39 2018
@Author: Abinash Mohanty
This is a network architecture file. 
Create networks similar to this and put in this folder. 
Add new networks to network.factory dictionary. 
"""

from .network import Network
import emulator as em

class testNet(Network):
	def __init__(self, ishardware=True, trainable=False):
		self.inputs = []
		self.trainable = trainable
		self.ishardware = ishardware
		self.framework = em	
		self.img = em.Placeholder(shape=[1, None, None, 3]) 
		self.layers = dict({'img':self.img})
		self.setup()

	def setup(self):
		(self.feed('img')
			 .max_pool(3,3,1,1, name='poolingTest', padding=1))	
			 #.conv(3, 3, 3, 1, 1, name='convv1', biased=False, relu=False, padding=1)
			 #.conv(3, 3, 3, 1, 1, name='convv2', biased=False, relu=False, padding=1))

