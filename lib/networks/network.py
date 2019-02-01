"""
Created on Tue May 01 10:46:55 2018
@Author: Abinash Mohanty
"""

import _init_paths
import emulator as em
#import tensorflow as tf
import cPickle as p
#from pvanet.config import cfg

DEFAULT_PADDING = 'SAME'
fraction_bits = 10
DEBUG_LEVEL = 2
WEIGHT_DECAY = 0.001
total_bits = 16

def include_original(dec):
    """ Meta decorator, which make the original function callable (via f._original() )"""
    def meta_decorator(f):
        decorated = dec(f)
        decorated._original = f
        return decorated
    return meta_decorator

@include_original
def layer(op):
    def layer_decorated(self, *args, **kwargs):
        name = kwargs.setdefault('name', self.get_unique_name(op.__name__))
        if len(self.inputs)==0:
            raise RuntimeError('No input variables found for layer %s.'%name)
        elif len(self.inputs)==1:
            layer_input = self.inputs[0]
        else:
            layer_input = list(self.inputs)
        layer_output = op(self, layer_input, *args, **kwargs)
        self.layers[name] = layer_output
        self.feed(layer_output)
        return self
    return layer_decorated

class Network(object):
	def __init__(self, inputs, parameters, ishardware=True, trainable=False):
		self.inputs = []
		self.layers = dict(inputs)
		self.ishardware = ishardware
		self.framework = em
		self.setup()

	def load(self, data_path, session, ignore_missing=False):
		"""
		Loads model to the network graph. 
		currently only cPickle file is supported. 
		input is path to the file
		"""
		if DEBUG_LEVEL >= 2:
			print 'loading models from : '+str(data_path)
		data_dict = p.load(open(data_path,'rb'))	
		for key in data_dict.keys():
			if key not in self.framework._all_variables:
				raise KeyError('Unknown layer in defined network: %s'%key)
		for key in self.framework._all_variables.keys():
			if key not in data_dict:
				raise KeyError('Value not defined in model for layer: %s'%key)
		for key in data_dict.keys():
			vv = self.framework.get_variable(key)
			vv.load(data_dict[key])

	def setup(self):
		raise NotImplementedError('Must be implemented in the subclass')

	def load(self):
		print 'Not yet implemented. Need to do this to load NN parameters.'
		
	def feed(self, *args):
		assert len(args) != 0
		self.inputs = []
		for layer in args:
			if isinstance(layer, basestring):
				try:
					if DEBUG_LEVEL >= 3:
						print layer
					layer = self.layers[layer]
				except KeyError:
					print self.layers.keys()
					raise KeyError('Unknown layer name fed: %s'%layer)
			self.inputs.append(layer)
		return self	
 
	def get_output(self,layer):
		"""
		Gives the output from a layer. 
		layer: name of the layer as specified in the network	
		"""				
		try:
			layer = self.layers[layer]
		except KeyError:
			print self.layers.keys()
			raise KeyError('Unknown layer name fed: %s'%layer)
		return layer

	def get_unique_name(self, prefix):
		id = sum(t.startswith(prefix) for t,_ in self.layers.items())+1
		return '%s_%d'%(prefix, id)

	def make_var(self, name, shape, initializer=None, trainable=True, regularizer=None):
		return self.framework.get_variable(name, shape, initializer=initializer, trainable=trainable, regularizer=regularizer)

	def validate_padding(self, padding):
		assert padding in ('SAME', 'VALID')

	@layer
	def conv(self, input, k_h, k_w, c_o, s_h, s_w, name, total_bits=total_bits, fraction_bits=fraction_bits, biased=True,relu=True, padding=DEFAULT_PADDING, trainable=True):
		#self.validate_padding(padding) TODO
		c_i = input.shape[-1]
		if self.ishardware:
			convolve = lambda i, k: self.framework.nn.conv2d(i, k, [1, s_h, s_w, 1], padding=padding, total_bits=total_bits, fraction_bits=fraction_bits)
		else:
			convolve = lambda i, k: self.framework.nn.conv2d(i, k, [1, s_h, s_w, 1], padding=padding)
			
		with self.framework.variable_scope(name) as scope:
			if self.ishardware:
				init_weights = None
				init_biases = None	
				regularizer= None
			else:
				init_weights = self.framework.contrib.layers.variance_scaling_initializer(factor=0.01, mode='FAN_AVG', uniform=False)
				init_biases = self.framework.constant_initializer(0.0)
				regularizer=self.l2_regularizer(WEIGHT_DECAY)

			kernel = self.make_var('weights', [k_h, k_w, c_i, c_o], init_weights, trainable, regularizer)
			if biased:
				biases = self.make_var('biases', [c_o], init_biases, trainable)
				conv = convolve(input, kernel)
				if relu:
					bias = self.framework.nn.bias_add(conv, biases)
					return self.framework.nn.relu(bias)
				return self.framework.nn.bias_add(conv, biases)
			else:
				conv = convolve(input, kernel)
				if relu:
					return self.framework.nn.relu(conv)
				return conv

	@layer
	def relu(self, input, name):
		return self.framework.nn.relu(input, name=name)
	
	@layer
	def max_pool(self, input, k_h, k_w, s_h, s_w, name, padding=DEFAULT_PADDING):
		#self.validate_padding(padding) TODO
		return self.framework.nn.max_pool(input,
			ksize=[1, k_h, k_w, 1],
			strides=[1, s_h, s_w, 1],
			padding=padding,
			name=name)
	
	@layer
	def avg_pool(self, input, k_h, k_w, s_h, s_w, name, padding=DEFAULT_PADDING):
		#self.validate_padding(padding) TODO
		return self.framework.nn.avg_pool(input,
			ksize=[1, k_h, k_w, 1],
			strides=[1, s_h, s_w, 1],
			padding=padding,
			name=name)

	@layer
	def reshape(self, input, d, name):
		input_shape = tf.shape(input)
		return self.framework.reshape(input,d)
	
	@layer
	def concat(self, inputs, axis, name):
		return tf.concat(axis=axis, values=inputs, name=name)

	@layer
	def fc(self, input, num_out, name, relu=True, trainable=True):
		with self.framework.variable_scope(name) as scope:
			if isinstance(input, tuple):
				input = input[0]
			input_shape = input.get_shape()
			if input_shape.ndims == 4:
				dim = 1
				for d in input_shape[1:].as_list():
					dim *= d
				feed_in = self.framework.reshape(self.framework.transpose(input, [0,3,1,2]), [-1, dim])	
			else:
				feed_in, dim = (input, int(input_shape[-1]))	

			if ishardware:
				init_weights = None
				init_biases = None
				regularizer = None	
			else:
				regularizer = self.l2_regularizer(WEIGHT_DECAY)
				if name == 'bbox_pred' :
					init_weights = self.framework.truncated_normal_initializer(0.0,stddev=0.001)
					init_biases = self.framework.constant_initializer(0.0)
				else:
					init_weights = self.framework.truncated_normal_initializer(0.0,stddev=0.01)			 
					init_biases = self.framework.constant_initializer(0.0)

			weights = self.make_var('weights', [dim, num_out], init_weights, trainable, \
                                    regularizer)
			biases = self.make_var('biases', [num_out], init_biases, trainable)

			op = self.framework.nn.relu_layer if relu else self.framework.nn.xw_plus_b
			fc = op(feed_in, weights, biases)
			return fc

	@layer
	def softmax(self, input, name):
		return self.framework.nn.softmax(input)

	@layer
	def add(self, input, name):
		# TEST FUNCTION
		a = input[0]
		b = input[1]
		return self.framework.nn.add(a,b)

	@layer
	def mult(self, input, name):
		# TEST FUNCTION
		a = input
		with self.framework.variable_scope(name) as scope:
			b = self.make_var('w', shape=[1])
		return self.framework.nn.mult(a,b)

	@layer
	def l2_regularizer(self, weight_decay=0.0005, scope=None):
		# TODO
		return None 
