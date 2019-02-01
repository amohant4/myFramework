"""
Created on Tue May 04 15:34:39 2018
@Author: Abinash Mohanty
"""

import emulator as em

class Variable():
	def __init__(self, shape, initial_value = None):
		self._shape = shape
		self.value = initial_value
		self.output_nodes = []
		em._default_graph.variables.append(self)

	@property
	def shape(self):
		"""
		API to get the shape of a variable
		return type is python list
		"""
		return self._shape

	def load(self, val):
		"""
		API to load values to a variable. 
		shape of the new value should be same as 
		the original shape of the variable. 
		Only supports numpy arrays as val. 
		"""	
		assert list(val.shape) == self._shape
		self.value = val
