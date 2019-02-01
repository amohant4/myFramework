"""
Created on Tue May 07 09:55:20 2018
@Author: Abinash Mohanty
"""

from emulator.operation import Operation 

class add(Operation):
	def __init__(self, a, b):
		super(add, self).__init__([a,b])
		self.shape = a.get_shape()

	def compute(self, var_a, var_b):
		self.inputs = [var_a, var_b]
		return var_a + var_b



