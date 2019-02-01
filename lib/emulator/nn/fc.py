"""
Created on Tue May 08 17:18:00 2018
@Author: Zheng Li, Abinash Mohanty
"""
import numpy as np
from emulator.operation import Operation


class FullLayer(Operation):
# class FullLayer(object):
    def __init__(self, input, W, b):
        # super(FullLayer,self).__init__([input])
        """
        Fully connected layer
        """
        # self.shape = input.get_shape()  # TODO
        self.shape = input.shape  # TODO
        self.W = W
        self.bias = b


    def compute(self, x):
        """
        Compute "forward" computation of fully connected layer
        """
        # x: (nb, ni), W: (ni, no), bias: (nb, no)
        # f_full = np.dot(x, self.W) + self.bias
        out = np.zeros((nb, no))
        for b in range(nb):
            for o in range(no):
                partial_sum = 0
                for i in range(ni):
                    partial_sum += x[b, i]*self.W[i, o]
                out[b, o] = partial_sum + self.bias[b, o]


        return out

