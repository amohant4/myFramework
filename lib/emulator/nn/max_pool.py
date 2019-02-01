"""
Created on Tue May 08 17:18:00 2018
@Author: Zheng Li, Abinash Mohanty
"""

import numpy as np
import emulator as em
from emulator.operation import Operation

class max_pool(Operation):
	def __init__(self, i, ksize, strides, padding, name):
		super(max_pool,self).__init__([i])
		self.ksize = ksize
		# print("i: ", i)
		# print("ksize: ", ksize)
		# print("strides: ", strides)
		# print("padding: ", padding)
		self.stride = strides
		self.padding = padding
		self._shape = [i.shape[0], None, None, i.shape[-1] ] 

	@property
	def shape(self):
		return self._shape 

	def pool_1ch(self, img_pad, ksize, stride):
		# print("img_ch shape: ", img_pad.shape)
		# print("img_ch: ", img_pad)

		ri, ci = img_pad.shape
		rk, ck = ksize[1], ksize[2]
		ro = int(np.floor((ri-rk)/stride[1])) + 1
		co = int(np.floor((ci-ck)/stride[2])) + 1
		pool_out = np.zeros((ro, co))
		pool_loc = np.zeros((ri, ci))
		for r in range(ro):
			for c in range(co):
				sr = r*stride[1]
				sc = c*stride[2]
				region_tmp = img_pad[sr:sr+rk, sc:sc+ck]
				pool_out[r, c] = np.max(region_tmp)
		return pool_out
	
	def compute(self, img):
		# print("img_ch shape: ", img.shape)
		# print("img_ch: ", img)
		img = img.astype(float)
	
		img_padded = em.utils.pad(img, self.ksize, self.stride, self.padding, padder = -999)
		img_b, img_h, img_w, img_c = img_padded.shape
		
		ro = int(np.floor((img_h-self.ksize[1])/self.stride[1]))+1
		co = int(np.floor((img_w-self.ksize[2])/self.stride[2]))+1
		
		pool_out = np.zeros((img_b, ro, co, img_c))
		
		for b_tmp in range(img_b):
			for i_tmp in range(img_c):
				pool_out_tmp = self.pool_1ch(img_padded[b_tmp,:,:,i_tmp], self.ksize, self.stride)
				pool_out[b_tmp,:,:,i_tmp] = pool_out_tmp
		return pool_out
