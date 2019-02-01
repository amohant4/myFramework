"""
Created on Tue May 02 15:34:39 2018
@Author: Abinash Mohanty
"""

from .testNet import testNet

def get_network(name, isHardware):
	return testNet(isHardware)
