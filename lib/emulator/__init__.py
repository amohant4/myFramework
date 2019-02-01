"""
Created on Tue May 07 09:55:20 2018
@Author: Abinash Mohanty
"""

import numpy as np
import nn as nn
import utils as utils
from .placeholder import Placeholder
from .graph import Graph
from .operation import Operation
from .variable import Variable
from .graph import Graph 
from .session import Session

# An graph instance is created with the emulator. 
# Currently only one graph is supported and is the default graph.
_default_graph = Graph()
_all_variables = {}
_global_var_scope = ''
_debug_level = 0

def set_default_graph(g):
	"""
	sets the given graph as default graph. 
	"""
	global _default_graph 
	_default_graph = g

def get_default_graph():
	"""
	Returns the default graph of the emulator
	this graph contains all variables, placeholders
	and operations defined in the the network object
	"""	
	return _default_graph

def set_debug_level(n):
	"""	
	Set the debug level of the emulator.
	5 -- it will print out all debug logs
	0 -- minimum logs printed
	"""	
	global _debug_level
	_debug_level = n 

# TODO: only uniform distribution is supported at the moment. 
def get_variable(name, shape=None, initializer=None, trainable=False, regularizer=None):
	"""
	API to create a new variable instance in the emulator. 
	If an variable already exists with the same name, it 
	will just return the existing variable. otherwise a new 
	instance is created. For new variables shape cannot be none. 
	"""
	global _global_var_scope	
	global _all_variables
	global _debug_level	

	if name in _all_variables:
		return _all_variables[name]

	name = _global_var_scope+'/'+name

	val = None
	assert shape is not None	
	if initializer is None:
		val = np.random.random_sample(shape)
	if _debug_level > 3:
		print 'Creating variable: '+name		
	v = Variable(shape, val)
	_all_variables[name] = v
	return v		

class variable_scope:
	"""
	Class to easily define variable scope. 
	"""	
	def __init__(self, name):
		self.name = name
	def __enter__(self):
		global _global_var_scope
		_global_var_scope = self.name
	def __exit__(self, type, value, traceback):
		global _global_var_scope 
		_global_var_scope = ''
