﻿#!/usr/bin/env/ python
################################################################################
#    Copyright (c) 2016 Brecht Baeten
#    This file is part of dympy.
#    
#    Permission is hereby granted, free of charge, to any person obtaining a
#    copy of this software and associated documentation files (the "Software"), 
#    to deal in the Software without restriction, including without limitation 
#    the rights to use, copy, modify, merge, publish, distribute, sublicense, 
#    and/or sell copies of the Software, and to permit persons to whom the 
#    Software is furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in 
#    all copies or substantial portions of the Software.
######################################################################################


try:
    import win32ui
    import dde
except Exception as e:
    print(e)
    
    print('The pywin32 version installed on the system is probably incompattible with dde used for communication between python2.7 and Dymola on windows')
    print('')
    print('To resolve this error:')
    print('1. Check your pywin32 version; it should be 214 (not 218) for those using v2.7')
    print('2. Delete pythonwin and pywin32_system32 folders entirely (presumably under C:\Python27\Lib\site-packages):')
    print('3. Download pywin32-214.win32-py2.7 from appropriate resources (one is: http://sourceforge.net/projects/pywin32/files/pywin32/Build%20214/ )')
    print('')
     
    print('Failed to import dde, the Dymola class can not be used')
   
   
import subprocess
import os
import inspect
import scipy.io
import string
import numpy as np
from shutil import copyfile,move

from . import util


class DymoBase(object):
    """
    Base class with common methods
    
    """
    def __init__(self,workingdir=None):
        """
        Initialize the data required for executing the dymosim.exe
        
        Parameters
        ----------
        workingdir : str
            path to a folder where the dymosim.exe file and dsin.txt files are
            located and where dsu.txt files and dsres files will be saved
        
        """
        
        # set the working dir
        if workingdir is None:
            self.workingdir = os.path.join( os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) , 'dymfiles' )
        else:
            self.workingdir = workingdir
    

        # create a copy of the original dsin.txt file if the copy does not exist
        if os.path.exists( os.path.join(self.workingdir ,'dsin.txt') ) and not os.path.exists( os.path.join(self.workingdir ,'dsin_original.txt') ):
            copyfile(os.path.join(self.workingdir ,'dsin.txt'),os.path.join(self.workingdir ,'dsin_original.txt'))
            
    
    def get_result(self):
        """
        Loads simulation results into a dictionary
        
        Returns
        -------
        res : dict
            dictionary with results, keys are the dymola variables as strings
            
        Examples
        --------
        >>> res = dymola.get_result()
        >>> res['test.A.B']
        
        """

        fileName = self.workingdir+'//dsres.mat'
        fullFileName = os.path.abspath(fileName)

        fileData = scipy.io.loadmat(fullFileName, matlab_compatible=True)

        name = fileData["name"].T
        description = fileData["description"].T
        dataInfo = fileData["dataInfo"].T
        data_1 = fileData["data_1"]
        data_2 = fileData["data_2"]

        namelist = []
        for item in name:
            #n = str(string.rstrip(string.join([x for x in item if len(x) > 0 and ord(x) < 128], "")))
            n = string.rstrip(''.join(item))

            if n =='Time':
                n = 'time'
            namelist.append(n)

        name = namelist
        
        res = {}
        for idx,item in enumerate(name):
            if dataInfo[idx,0] == 1:
                #add the single value of a parameter
                res[item] = np.array([scipy.sign(dataInfo[idx,1])*data_1[abs(dataInfo[idx,1])-1][0]])
            
                # create a linspace vector with the same length as data
                #res[item] = scipy.sign(dataInfo[idx,1]) * scipy.linspace(data_1[abs(dataInfo[idx,1])-1][0], data_1[abs(dataInfo[idx,1])-1][1], len(data_2[0]) )
            else:
                res[item] = scipy.sign(dataInfo[idx,1]) * data_2[abs(dataInfo[idx,1])-1]
        
        # store and return the results
        self.res = res
        return res
           

    def write_dsu(self,data):
        """
        Writes a dsu file which will be used by dymola as input
        
        Parameters
        ----------
        data : dict
            with name - value pairs, 'time' must be a key
        
        Raises
        ------
        InputError
            If no 'time' key is supplied
        
        Examples
        --------
        >>> dymola.write_dsu({'time':[0,43200,86400],'u':[1000,5000,2000]})
        
        """
        
        # check if time is a key of the inputdata
        if not 'time' in data:
            raise InputError('The supplied input data did not contain a \'time\' key')
        
        filename = os.path.join(self.workingdir,'dsu.txt')
        util.savemat(filename,data,['time'])
      

      


class Dymola(DymoBase):
    """
    Class which governs the connection to Dymola
    
    """
    def __init__(self):
        """
        Initializes a new dymola object and tries to connect with Dymola

        Examples
        --------
        >>> dymola = dympy.Dymola()
        
        """
        
        super(Dymola,self).__init__()
        
        self.connect()
        
        
        self.workingdir = os.path.join( os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) , 'dymfiles' )
        self.run_cmd('cd("'+self.workingdir+'");')

        # clear ds files from the working dir
        try:
            os.remove(self.workingdir+'//dsu.txt') 
            os.remove(self.workingdir+'//dsin.txt') 
            os.remove(self.workingdir+'//dsfinal.txt') 
            os.remove(self.workingdir+'//dslog.txt')
            os.remove(self.workingdir+'//buildlog.txt')
            os.remove(self.workingdir+'//dsres.mat') 
            os.remove(self.workingdir+'//dsmodel.c')
            os.remove(self.workingdir+'//dymosim.exe')
            os.remove(self.workingdir+'//dymosim.exp')
            os.remove(self.workingdir+'//dymosim.lib')
        except:
            pass
            
    
    def connect(self):
        """
        Tries to create a connection to dymola
        
        """
        
        self._server = dde.CreateServer()
        self._server.Create('dym')
        self._conversation = dde.CreateConversation(self._server)
        
        # try to connect to dymola    
        try:
            self._conversation.ConnectTo('Dymola','cd("C://");')
        except:
            # dymola is probably not opened so try to open it first end wait some time before retrying
            subprocess.Popen(['dymola'])
            time.sleep(10)
            
            try:
                self._conversation.ConnectTo('Dymola','cd("C://");')
            except:
                raise Exception('Dymola could not be found')
                
                
    def disconnect(self):
        """
        Shuts down the dde server
        
        """
        
        self._server.Shutdown()
    
    
    def openModel(self,filename):    
        """
        Opens a .mo file in Dymola
        
        Parameters
        ----------
        filename : string
            the name of the file
            
        Examples
        --------
        >>> dymola.openModel('C:\\Python27\\Lib\\site-packages\\dympy\\test.mo')
        
        """
        
        self.run_cmd('openModel("{}",true);'.format(os.path.abspath(filename)))
        
        # cd back to the working dir afterwards
        self.run_cmd('cd("'+self.workingdir+'");')
        

    def clear(self):
        """
        Closes all models opened in Dymola
        
        """
        
        self.run_cmd('clear()')
    
    
    def compile(self,modelname,parameters=None):
        """
        Compiles a modelica model with optional parameters
        
        Parameters
        ----------
        modelname : string
            the name of the model
            
        parameters : dict
            optional dictionary of parameters to compile with the model
        
        Examples
        --------
        >>> dymola.compile('test')
        >>> dymola.compile('test',parameters={'A':5})
        
        """
        
        if parameters == None:
            arguments = ''
        else:
            argumentslist = []
            for key,val in parameters.items():
                if isinstance(val,np.ndarray):
                    if len(val.shape)==1:
                        vallist = []
                        for v in val:
                            vallist.append(str(v))
                        argumentslist.append('{}=vector([{}])'.format(key,','.join(vallist)))
                    else:
                        print('Warning: multi dimensional array assignment is not yet supported')
                else:
                    argumentslist.append('{}={}'.format(key,val))
                
            arguments = ','.join(argumentslist)
                
        problem = '"{modelname}({arguments})"'.format(modelname=modelname,arguments=arguments)

        self.run_cmd('translateModel(problem={problem})'.format(problem=problem))
    
    
    def simulate(self,StartTime=0,StopTime=1,OutputInterval=0,NumberOfIntervals=500,Tolerance=1e-4,FixedStepSize=0,Algorithm='dassl'):
        """
        Simulates a compiled model
        
        Parameters
        ----------
        StartTime : number
            simulation start time in seconds
            
        StopTime : number
            simulation stop time in seconds
            
        OutputInterval : number
            interval between the output data in seconds
            
        NumberOfIntervals : int
            number of intervals in the output data, if both OutputInterval and 
            NumberOfIntervals are > 0 ???
            
        Tolerance : number
            integration tolerance
            
        FixedStepSize : number
            interval between simulation points used with fixed timestep methods
            
        Algorithm : string
            integration algorithm ['dassl','lsodar','euler',...]
        
        Examples
        --------
        >>> dymola.simulate(StopTime=86400)
        
        """
        
        self.run_cmd('experiment(StartTime=%s,StopTime=%s,OutputInterval=%s,NumberOfIntervals=%s,Tolerance=%s,FixedStepSize=%s,Algorithm="%s"); simulate();'%(StartTime,StopTime,OutputInterval,NumberOfIntervals,Tolerance,FixedStepSize,Algorithm))
        
        
    def set_parameters(self,pardict):
        """
        Sets all values in the parameter dictionary to their value
        
        Parameters
        ----------
        pardict : dict
            name - value pairs for parameters
            
        Notes
        -----
        The parametes must be free to vary after compilation in modelica, this 
        often requires setting :code`annotation(Evaluate=false)` for the
        parameter. If not parameters must be supplied during the model
        compilation
        
        Examples
        --------
        >>> dymola.set_parameters({'C1.T':300})
        
        """
        
        # write to dympy.mos
        f = open( self.workingdir+'//dympy.mos', 'w')
        for key,val in pardict.items():
            f.write( '%s=%s\n'%(key,val) )

        f.close()
        self.run_cmd( 'RunScript("dympy.mos")' )

                
    def dsfinal2dsin(self):
        """
        Import dsfinal.txt as initial condition
        
        Examples
        --------
        >>> dymola.dsfinal2dsin()
        
        """
        
        self.run_cmd('importInitial("dsfinal.txt");')
        
        
    def run_cmd(self,cmd):
        """
        Runs a Dymola command
        
        Parameters
        ----------
        par : string
        
        Examples
        --------
        >>> dymola.run_cmd('clear()')
        
        """
        try:
            self._conversation.Exec(cmd)
        except Exception as e:
            print(e)
            
            
    def __del__(self):
        """
        Disconnect the dde server before deleting the object
        
        """
        
        self.disconnect()
        
        
        
        
class Dymosim(DymoBase):
    """
    Class to run simulations with a pre-compiled Dymola model as a
    dymosim.exe file
    """
    
    def __init__(self,workingdir=None):
        """
        Initialize the data required for executing the dymosim.exe
        
        Parameters
        ----------
        workingdir : str
            path to a folder where the dymosim.exe file and dsin.txt files are
            located and where dsu.txt files and dsres files will be saved
        
        """
    
        super(Dymosim,self).__init__(workingdir=workingdir)
  
            
    def simulate(self,StartTime=0,StopTime=1,OutputInterval=0,NumberOfIntervals=500,Tolerance=1e-4,FixedStepSize=0,Algorithm='dassl'):
        
        algorithms = {
            'deabm':   1,
            'lsode1':  2,
            'lsode2':  3,
            'lsodar':  4,
            'dopri5':  5,
            'dopri8':  6,
            'grk4t':   7,
            'dassl':   8,
            'odassl':  9,
            'mexx':   10,
            'euler':  11,
            'rkfix2': 12,
            'rkfix3': 13,
            'rkfix4': 14,
        }

        # edit the dsin file
        oldpath = os.path.join(self.workingdir ,'dsin.txt')
        newpath = os.path.join(self.workingdir ,'newdsin.txt')
        with open(oldpath) as oldfile:
            with open(newpath) as newfile:

                for line in oldfile:
                    if '# StartTime    Time at which integration starts' in line:
                        line = ' {} # StartTime    Time at which integration starts'.format(StartTime)
                    elif '# StopTime     Time at which integration stops' in line:
                        line = ' {} # StopTime     Time at which integration stops'.format(StopTime)
                    elif '# Increment    Communication step size, if > 0' in line:
                        line = ' {} # Increment    Communication step size, if > 0'.format(OutputInterval)
                    elif '# nInterval    Number of communication intervals, if > 0' in line:
                        line = ' {} # nInterval    Number of communication intervals, if > 0'.format(NumberOfIntervals)
                    elif '# Tolerance    Relative precision of signals for' in line:
                        line = ' {} # Tolerance    Relative precision of signals for'.format(Tolerance)
                    elif '# MaxFixedStep Maximum step size of fixed step size' in line:
                        line = ' {} # MaxFixedStep Maximum step size of fixed step size'.format(FixedStepSize)
                    elif '# Algorithm    Integration algorithm as integer (1...28)' in line:
                        line = ' {} # Algorithm    Integration algorithm as integer (1...28)'.format(algorithms[Algorithm])
                    
                    
                    newfile.write(line)
        
        
        os.remove(oldpath)
        move(newpath, oldpath)
        
        
        # run the process
        subprocess.call([os.path.join(self.workingdir ,'dymosim.exe')])
    
    
    def set_parameters(self,pardict):
        """
        Sets all values in the parameter dictionary to their value
        
        Parameters
        ----------
        pardict : dict
            name - value pairs for parameters
            
        Notes
        -----
        The parametes must be free to vary after compilation in modelica, this 
        often requires setting :code`annotation(Evaluate=false)` for the
        parameter. If not parameters must be supplied during the model
        compilation
        
        Examples
        --------
        >>> dymosim.set_parameters({'C1.T':300})
        
        """
        
        # copy dsin_original.txt to dsin.txt
        if os.path.exists(os.path.join(self.workingdir ,'dsin_original.txt')):
            try:
                os.remove(os.path.join(self.workingdir ,'dsin.txt'))
            except:
                pass
            
            copyfile(os.path.join(self.workingdir ,'dsin_original.txt'),os.path.join(self.workingdir ,'dsin.txt'))
        else:
            print('Warning: dsin_original.txt does not exist, assuming the dsin.txt file is the original file')
        
        
        # write to dsin.txt
        for key,val in pardict.items():
            pass
        
    
    def dsfinal2dsin(self):
        """
        Import dsfinal.txt as initial condition
        
        Examples
        --------
        >>> dymosim.dsfinal2dsin()
        
        """
        
        # remove the old dsin.txt
        try:
            os.remove(os.path.join(self.workingdir ,'dsin.txt'))
        except:
            pass
            
        # copy dsfinal.txt to dsin.txt    
        copyfile(os.path.join(self.workingdir ,'dsfinal.txt'),os.path.join(self.workingdir ,'dsin.txt'))

        