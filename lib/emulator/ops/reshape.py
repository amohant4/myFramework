"""
Created on Tue May 14 14:32:00 2018
@Author: Abinash Mohanty
"""

from emulator.operation import Operation 

class reshape(Operation):
	def __init__(self, a):
		super(reshape, self).__init__([a,b])
		self.shape = a.get_shape()

	def compute(self, var_a):
   pass