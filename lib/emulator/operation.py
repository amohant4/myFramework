"""
Created on Tue May 04 15:34:39 2018
@Author: Abinash Mohanty
"""

import emulator as em

class Operation(object):
	def __init__(self, input_nodes = []):
		self.input_nodes = input_nodes
		self.output_nodes = []
		
        # For every node in the input, we append this operation (self) to the list of
        # the consumers of the input nodes
		for node in input_nodes:
			node.output_nodes.append(self)

        # There will be a global default graph (TensorFlow works this way)
        # We will then append this particular operation
        # Append this operation to the list of operations in the currently active default graph
		em._default_graph.operations.append(self)

	@property
	def shape(self):
		raise NotImplementedError('Must be implemented in the subclass')

	def compute(self):
		"""
		Must be implemented in the sub class. 
		"""	
		raise NotImplementedError('Must be implemented in the subclass')
