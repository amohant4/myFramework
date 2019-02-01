"""
Created on Tue May 04 15:34:39 2018
@Author: Abinash Mohanty
"""

import numpy as np
from .operation import Operation
from .placeholder import Placeholder
from .variable import Variable

class Session:
	def traverse_postorder(self,operation):
		nodes_postorder = []
		def recurse(node):
			if isinstance(node, Operation):
				for input_node in node.input_nodes:
					recurse(input_node)
			nodes_postorder.append(node)
		recurse(operation)
		return nodes_postorder

	def run(self, operation, feed_dict = {}):
		nodes_postorder = self.traverse_postorder(operation)
		for node in nodes_postorder:
			if isinstance(node, Placeholder):
				node.output = feed_dict[node]
			elif isinstance(node, Variable):
				node.output = node.value
			else:
				node.inputs = [input_node.output for input_node in node.input_nodes]
				node.output = node.compute(*node.inputs)
			if type(node.output) == list:
				node.output = np.array(node.output)
		return operation.output
