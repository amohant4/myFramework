"""
Created on Tue May 11 11:39:00 2018
@Author: Zheng Li, Abinash Mohanty
"""

import numpy as np
import emulator as em
from emulator.operation import Operation


class conv2d(Operation):
	def __init__(self, i, k, stride, padding, total_bits=None, fraction_bits=None):
		super(conv2d, self).__init__([i,k])	# Must call this function with the inputs (inputs needed for computation)
		self.padding = padding	
		self.kernel = k
		self.stride = stride
		# print("self.padding: ", self.padding)
		# print("self.kernel: ", self.kernel)
		# print("self.stride: ", self.stride)
		self.total_bits = total_bits
		self.fraction_bits = fraction_bits
		self._shape = [i.shape[0], None, None, k.shape[-1]] 	# Must be done here. It will throw errors otherwise. Height and Width can be left as none here

	@property
	def shape(self):
		return self._shape 

	def _conv_1ch(self, img_pad, kernel, stride):
		kh, kw = kernel.shape
		hi, wi = img_pad.shape
		ho = int((np.floor(hi-kh)*1.0/stride[1]))+1
		wo = int((np.floor(wi-kw)*1.0/stride[2]))+1
		output = np.zeros(shape=(ho, wo))
		# print("kernel: ", kernel)

		for i in range(ho):
			for j in range(wo):
				si = i*stride[1]
				sj = j*stride[2]
				partial_sum = 0
				for mm in range(kh):
					for nn in range(kw):
						partial_sum += (img_pad[si+mm, sj+nn]*kernel[mm, nn])
				output[i, j] = partial_sum
		return output

	def compute(self, img, kernel):
		img_padded = em.utils.pad(img, kernel.shape, self.stride, self.padding, padder = 0)

		img_b, img_h, img_w, img_c = img_padded.shape
		# k_h, k_w, c_i, c_o = kernel.shape
		c_o, c_i, k_h, k_w = kernel.shape

		ho = int((np.floor(img_h - k_h)*1.0/self.stride[1]))+1
		wo = int((np.floor(img_w - k_w)*1.0/self.stride[2]))+1

		y = np.zeros((img_b, ho, wo, c_o))

		for o_tmp in range(c_o):
			for b_tmp in range(img_b):
				for i_tmp in range(c_i):
					out_ch1 = self._conv_1ch(img_padded[b_tmp,:,:,i_tmp], kernel[o_tmp,i_tmp,:,:], self.stride)
					y[b_tmp,:,:,o_tmp] = y[b_tmp,:,:,o_tmp] + out_ch1
		return y
