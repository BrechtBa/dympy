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


import numpy as np
import scipy.io

def get_value_array(res,key):
    """
    Creates and array of result keys with the same name but differtent indices
    
    Parameters
    ----------
    res : dict
        results dictionary
        
    key : string
        variable name
    
    Returns
    -------
    val : numpy.ndarray
        nd array with values
        
    Examples
    --------
    >>> get_value_array({'time':[0,43200,86400],'u[1]':[1000,5000,2000],'u[2]':[2000,8000,3000]},'u')
    
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
    
def get_children(res,key):
    """
    Returns a list with all keys in res starting with key
    
    Parameters
    ----------
    res : dict
        results dictionary
    
    key : string
        a search key
        
    Returns
    -------
    keys : list
        list of keys that start with key
        
    Examples
    --------
    >>> get_keys_with({'time':[0,43200,86400],'A.B':[1000,5000,2000],'A.C':[2000,8000,3000]},'A')
    
    """
    
    if key == '':
        return res.keys()
    else:
        keys = []
        for k in res.keys():
            if k.startswith(key):
                keys.append(k)
                
        return keys    
            
    
def savemat(filename,data,order=None):
    """
    Writes a binary file which can be loaded by dymola
    
    Parameters
    ----------
    data : dict
        dictionary with name, value pairs
        
    order : list
        list of keys representing the order of the data in the saved file
        
    Examples
    --------
    >>> savemat({'time':[0,43200,86400],'u':[1000,5000,2000]})
    
    """
     
    Aclass = ['Atrajectory          ',
              '1.0                  ',
              'Generated from Matlab']
    
    # make sure time is the first element
    names,values = dict2list(data,order)

    values = zip(*data)
    
    scipy.io.savemat( filename, {'Aclass': Aclass}, appendmat=False, format='4')
    with open(filename, 'ab') as f:
        scipy.io.savemat(f, {'names': names}, format='4')
    with open(filename, 'ab') as f: 
        scipy.io.savemat(f, {'data': values}, format='4')
        
        
def dict2list(data,order=None):
    """
    Converts a dictionary to a list of keys and a list of values
    
    Parameters
    ----------
    data : dict
        dictionary with name, value pairs
        
    order : list
        list of keys representing the order of the data in the saved file
        
    Examples
    --------
    >>> dict2list({'time':[0,43200,86400],'u':[1000,5000,2000]})
    
    """
    
    names = []
    # first add the keys in order
    if order!=None:
        for key in order:
            names.append(key)
            
    # add the rest    
    for key in data:
        if not key in names:
            names.append(key)
    
    # create the values list
    values = []
    for key in names:
        values.append(data[key])
    
    return names,values
