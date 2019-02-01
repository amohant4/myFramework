"""
Created on Tue May 11 17:41:00 2018
@Author: Abinash Mohanty
"""

from emulator.operation import Operation 

class avg_pool(Operation):
	def __init__(self, input, k_size, strides, padding):
		super(avg_pool,self).__init__([input])
		self.kernel = k_size
		self.stride = strides
		self.padding = padding
		self.shape = input.get_shape()  # TODO

	def compute(self, input):
		return input
