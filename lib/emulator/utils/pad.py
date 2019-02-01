"""
Created on Tue May 21 10:27:00 2018
@Author: Abinash Mohanty
Python lib with helper functions for padding.
"""

import numpy as np

def _get_padding_value(img, kernel_shape, stride, padding):
	"""
	Returns the padding values along different axis. 
	"""
	if isinstance(padding, basestring):	# it can be SAME, VALID : used for tensorflow type
		# calculate padding values here
		# to get the shape of the input and kernel
		# call img.shape and kernel.shape 
		# because img and kernel will be numpy arrays here.
		# we need to call these at runtime and not at the 
		# constructor because image size can be variable
		shape = img.shape
		if padding == 'VALID':
			return 0		
		elif padding == 'SAME':
			ri = shape[1]
			kr = kernel_shape[0]
			ro = np.ceil(ri/stride[1])
			pr_t = np.floor(((ro-1)*stride[1]+kr-ri)/2)
			pr_b = np.ceil(((ro-1)*stride[1]+kr-ri)/2)
			ci = shape[2]
			kc = kernel_shape[1]
			co = np.ceil(ci/stride[2])
			pc_l = np.floor(((co-1)*stride[2]+kc-ci)/2)
			pc_r = np.ceil(((co-1)*stride[2]+kc-ci)/2)
			return ((int(pr_t), int(pr_b)), (int(pc_l), int(pc_r)))		
	elif isinstance(padding, int):			# emulator padding (TODO) 
		# this is similar to caffe at the moment
		# we directly pass the padding value 
		# padding in all directions is same
		# should make it the way you have it
		return padding

def _pad_with(array, pad_width, iaxis, kwargs):
	pad_value = kwargs.get('padder', 0)
	array[:pad_width[0]] = pad_value
	array[-pad_width[1]:] = pad_value
	return array

def pad(img, kernel_shape, stride, padding):
	"""
	Call this function to get the padded output.
	img: input feature map
	kernel_shape: shape of kernel
	stride: stride along all axis
	padding: padding value
	"""	
	batch_size, img_height, img_width, c_in = img.shape
	pad_value = _get_padding_value(img, kernel_shape, stride, padding)

	if isinstance(pad_value, tuple):	# TODO check this 
		vertical_pad_width = pad_value[0][0] + pad_value[0][1] 
		horizontal_pad_width = pad_value[1][0] + pad_value[1][1]
	else:			
		vertical_pad_width = 2*pad_value
		horizontal_pad_width = 2*pad_value

	img_padded = np.empty((batch_size, img_height + vertical_pad_width , img_width + horizontal_pad_width, c_in))

	for batch in range(batch_size):
		for ch in range(c_in):
			img_padded[batch,:,:,ch] = np.pad(img[batch,:,:,ch], pad_value, _pad_with, padder=0)

	return img_padded
