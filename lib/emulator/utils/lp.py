"""
Created on Tue Apr 23 08:45:28 2018
@Author: Abinash Mohanty
Python lib with helper functions for fixed point arithemetic.
"""

import numpy as np
import math
import os.path

print 'Loading low precision utils from : ' + str(os.path.abspath(__file__))

def get_random_number(low=0, high=255):	
	"""
	Returns a random number in the range provided. 
	low - lower bound of the random number range. Default value: 0
	high - higher bound of the random number range Defalt value: 255
	return - random int in the range
	"""
	return np.random.randint(0,255)

def getFixedPoint(num, totalBits, fractionBits, mode=0):
	"""
	Returns a fixed point value of num. 
	num - input number
	totalBits - total number of bits
	fractionBits - number of fractional bits
	mode - 0: returns str, 1: returns float
	"""
	if isinstance(num, basestring):
	    num = float(num)
	sign = 1
	if num < 0:
		sign = -1
	if mode == 1:
		return sign*round(abs(num)*pow(2,fractionBits))/pow(2,fractionBits)
	return str(sign*round(abs(num)*pow(2,fractionBits))/pow(2,fractionBits))

def getFixedPointBinary(num, totalBits, fractionBits):
	"""
	Returns a fixed point value of num. 
	num - input number
	totalBits - total number of bits
	fractionBits - number of fractional bits
	"""
	# Modified for take care of signed fixed point numbers
	if isinstance(num, basestring):
	    num = float(num)
	sign = 1
	if num < 0:
	    sign = -1
	nn = sign*int(round(abs(num)*pow(2, fractionBits)))
	binString = bin(((1 << totalBits) - 1) & nn)
	if binString.find('b')!=-1:
	    return binString.split('b')[1].zfill(totalBits)
	return binString.zfill(totalBits)

def getIntFromBinary(numString):
	"""
	returns the integer value represented by the binary number
	Only +ve numbers for now 
	TODO 
	"""
	return int(numString, 2)
