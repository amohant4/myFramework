"""
Created on Tue May 11 12:01:00 2018
@Author: Abinash Mohanty
"""

from emulator.operation import Operation 


class bias_add(Operation):
	def __init__(self, i, b):
		super(bias_add, self).__init__([i,b])
		self.shape = i.get_shape()

	def compute(self, i, b):
		self.inputs = [i, b]
		return i

		
