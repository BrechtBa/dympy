#!/usr/bin/python
######################################################################################
#    Copyright 2015 Brecht Baeten
#    This file is part of dympy.
#
#    dympy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    dympy is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with dympy.  If not, see <http://www.gnu.org/licenses/>.
######################################################################################

# if an error like this arises:
# Traceback (most recent call last):
#  File "C:\IQTrader\_script\_obj\DDEClient.py", line 12, in <module>
#   import dde
# ImportError: This must be an MFC application - try 'import win32ui' first
# 
# 1.Delete pythonwin and pywin32_system32 folders entirely (presumably under C:\Python27\Lib\site-packages)
# 2.Check your pywin32 version; it should be 214 (not 218) for those using v2.7
# 3.Download pywin32-214.win32-py2.7 from appropriate resources (one is this: http://sourceforge.net/projects/pywin32/files/pywin32/Build%20214/ )

import numpy as np
import scipy.io


def get_value_array(res,key):
	"""
	creates and arry of result keys with the same name
	
	Arguments:
	res: result dict
	key: string
	
	Example:
	get_value_array({'time':[0,43200,86400],'u[1]':[1000,5000,2000],'u[2]':[2000,8000,3000]},'u')
	"""
	
	# find the dimensions of the result
	for k in res:
		if key + '[' == k[:len(key)+1]:
			index_string = k[len(key):-1]
			print(index_string)
			
			temp_index_list = np.array([int(x) for x in index_string.split(',')])
			try:
				index_list = np.maximum(index_list,temp_index_list)
			except:
				index_list = temp_index_list
	
	# create an empty value array	
	val = np.zeros(np.append(len(res['time']),index_list))
	
	# fill the array by iterating over all dimensions
	it = np.nditer(val[0,:],flags=['multi_index'])
	while not it.finished:
	
		index_string = '{}'.format(it.multi_index)[1:-1].replace(' ','')
		val[(Ellipsis,)+it.multi_index] = res[ key + '[{}]'.format(index_string)]
		it.iternext()
	
	return val
	
	
def savemat(filename,inputdict,order=None):
	"""
	writes a binary file which can be loaded by dymola
	
	Arguments:
	inputdict: dictionary with name, value pairs, 'time' must be a key
	
	Example:
	savemat({'time':[0,43200,86400],'u':[1000,5000,2000]})
	"""
	Aclass = ['Atrajectory          ',
			  '1.0                  ',
			  'Generated from Matlab']
	
	# make sure time is the first element
	names,data = dict2list(inputdict,order)

	data = zip(*data)
	
	scipy.io.savemat( filename, {'Aclass': Aclass}, appendmat=False, format='4')
	with open(filename, 'ab') as f:
		scipy.io.savemat(f, {'names': names}, format='4')
	with open(filename, 'ab') as f: 
		scipy.io.savemat(f, {'data': data}, format='4')
		
		
def dict2list(inputdict,order=None):

	names = []
	# first add the keys in order
	if order!=None:
		for key in order:
			names.append(key)
			
	# add the rest	
	for key in inputdict:
		if not key in names:
			names.append(key)
	
	# create the data matrix
	data = []
	for key in names:
		data.append(inputdict[key])
	
	return names,data
