"""
Created on Tue May 11 12:02:00 2018
@Author: Abinash Mohanty
"""

from emulator.operation import Operation 

class relu(Operation):
	def __init__(self, i):
		super(relu, self).__init__([i])
		self.shape = i.get_shape()
	
	def compute(self, i):
		return i
