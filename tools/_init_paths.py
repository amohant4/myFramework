# Initialize the paths to library. Adds the Utils folder to the python path
# Author	: Abinash Mohanty
# Date 		: 04/23/2018
# Assumes that the file is in demo dir. Change otherwise

import os
import os.path as osp
import sys

def add_path(path):
	"""
	This function adds path to python path. 
	"""
	if path not in sys.path:
		sys.path.insert(0,path)

lib_path = osp.abspath(osp.join(osp.dirname(__file__), '..', 'lib'))
add_path(lib_path)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
