"""
Created on Tue May 04 15:34:39 2018
@Author: Abinash Mohanty
"""

import emulator as em

class Placeholder():
	def __init__(self, shape):
		self.output_nodes = []
		self._shape = shape
		em._default_graph.placeholders.append(self)

	@property
	def shape(self):
		return self._shape

