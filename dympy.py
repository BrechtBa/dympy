

# if an error like this arises:
# Traceback (most recent call last):
#  File "C:\IQTrader\_script\_obj\DDEClient.py", line 12, in <module>
#   import dde
# ImportError: This must be an MFC application - try 'import win32ui' first
# 
# 1.Delete pythonwin and pywin32_system32 folderes entirely (presumably under C:\Python27\Lib\site-packages)
# 2.Check your pywin32 version; it should be 214 (not 218) for those using v2.7
# 3.Download pywin32-214.win32-py2.7 from appropriate resources (one is this: http://sourceforge.net/projects/pywin32/files/pywin32/Build%20214/ )

import win32ui
import dde
import os
import scipy.io
import string

class Dymola:
	def __init__(self):
		"""
		initializes a new dymola object
		
		Example:
		import dympy
		dymola = dympy.Dymola()
		"""
		
		self._server = dde.CreateServer()
		self._server.Create('dym')
		self._conversation = dde.CreateConversation(self._server)
		self._conversation.ConnectTo('Dymola','cd("C://");')
		
		self.res = {}
		self.workingdir = 'C://Python27//Lib//site-packages//dympy//dymfiles'
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
		
	def openModel(self,filename):	
		"""
		Opens a .mo file in Dymola
		
		Example:
		dymola.openModel('C:\\Python27\\Lib\\site-packages\\dympy\\test.mo')
		"""
		self.run_cmd('openModel("'+ os.path.abspath(filename) +'",true);')
		
		# cd back to the working dir afterwards
		self.run_cmd('cd("'+self.workingdir+'");')
		
	def clear(self):
		"""
		Closes all models opened in Dymola
		"""
		self.run_cmd('clear()')
	
	def compile(self,modelname):
		"""
		Compiles a modelica model
		
		Example:
		dymola.compile('test')
		"""
		self.run_cmd('translateModel("'+ modelname +'")')
	
	def simulate(self,StartTime=0,StopTime=1,OutputInterval=0,NumberOfIntervals=500,Tolerance=1e-4,FixedStepSize=0,Algorithm='dassl'):
		"""
		Simulates a compiled model
		
		Arguments:
		StartTime = 0
		StopTime = 1
		OutputInterval = 0
		NumberOfIntervals = 500
		Tolerance = 1e-4
		FixedStepSize = 0
		Algorithm = 'dassl'
		
		Example:
		dymola.simulate(StopTime=86400)
		"""
		
		self.run_cmd('experiment(StartTime=%s,StopTime=%s,OutputInterval=%s,NumberOfIntervals=%s,Tolerance=%s,FixedStepSize=%s,Algorithm="%s");'%(StartTime,StopTime,OutputInterval,NumberOfIntervals,Tolerance,FixedStepSize,Algorithm))
		self.run_cmd('simulate();')
		
	def set_parameters(self,pardict):
		"""
		sets all values in the parameter dictionary to their value
		Arguments:
		pardict: dictionary with name, value pairs
		
		Example:
		dymola.set_parameters({'C1.T':300})
		"""
		
		# write to dympy.mos
		f = open( self.workingdir+'//dympy.mos', 'w')
		for key,val in pardict.iteritems():
			f.write( '%s=%s\n'%(key,val) )

		f.close()
		self.run_cmd( 'RunScript("dympy.mos")' )

				
	def get_result(self):
		"""
		loads results into a dictionary
		
		Example:
		res = dymola.get_result()
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
			n = string.rstrip(string.join(item,''))

			if n =='Time':
				n = 'time'
			namelist.append(n)

		name = namelist
		
		res = {}
		for idx,item in enumerate(name):
			if dataInfo[idx,0] == 1:
				# create a linspace  vector with the same length as data
				res[item] = scipy.sign(dataInfo[idx,1]) * scipy.linspace(data_1[abs(dataInfo[idx,1])-1][0], data_1[abs(dataInfo[idx,1])-1][1], len(data_2[0]) )
			else:
				res[item] = scipy.sign(dataInfo[idx,1]) * data_2[abs(dataInfo[idx,1])-1]
		
		# store and return the results
		self.res = res
		return res

	def write_dsu(self,inputdict):
		"""
		writes a dsu file which will be used as input
		
		Arguments:
		inputdict: dictionary with name, value pairs, 'time' must be a key
		
		Example:
		dymola.write_dsu({'time':[0,43200,86400],'u':[1000,5000,2000]})
		"""
		Aclass = ['Atrajectory          ',
				  '1.0                  ',
				  'Generated from Matlab']
	  
		names = []
		data = []
		# make sure time is the first element
		for key in inputdict:
			if key == 'time':
				names.append(key)
				data.append(inputdict[key])
		
		for key in inputdict:
			if key != 'time':
				names.append(key)
				data.append(inputdict[key])
		
		data = zip(*data)
		
		filename = self.workingdir+'\\dsu.txt'
		
		scipy.io.savemat( filename, {'Aclass': Aclass}, appendmat=False, format='4')
		with open(filename, 'ab') as f:
			scipy.io.savemat(f, {'names': names}, format='4')
		with open(filename, 'ab') as f: 
			scipy.io.savemat(f, {'data': data}, format='4')	
			
	def get_res(self,par):
		"""
		returns a list with all parameters starting with parameter or the value of the parameter if there is only one
		"""
		if par == '':
			return self.res.keys()
		else:
			if par in self.res.keys():
				return self.res[par]
			else:
				names = []
				for key in self.res.keys():
					if key.startswith(par):
						names.append(key)
						
				return names
				
	def dsfinal2dsin(self):
		"""
		import dsfinal.txt as initial condition
		"""
		self.run_cmd('importInitial("dsfinal.txt");')
		
		
	def run_cmd(self,cmd):
		"""
		Runs a Dymola command after initialization
		"""
		self._conversation.Exec(cmd)
		