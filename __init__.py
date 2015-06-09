

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
	
		self._server = dde.CreateServer()
		self._server.Create('dym')
		self._conversation = dde.CreateConversation(self._server)
		self._conversation.ConnectTo('Dymola','cd("C://")')
		
	def run_cmd(self,cmd):
		"""
		Runs a Dymola command after initialization
		"""
		self._conversation.Exec(cmd)
		
	def openModel(self,filename):	
		"""
		Opens a .mo file in Dymola
		"""
		self.run_cmd('openModel("'+ filename +'",true);')
		
	def compile(self,modelname):
		"""
		Compiles a modelica model
		"""
		self.run_cmd('translateModel("'+ modelname +'")')

	def simulate(self,StartTime=0,StopTime=1,OutputInterval=0,NumberOfIntervals=500,Tolerance=1e-4,FixedStepSize=0,Algorithm='dassl'):
		"""
		Arguments:
		StartTime = 0
		StopTime = 1
		OutputInterval = 0
		NumberOfIntervals = 500
		Tolerance = 1e-4
		FixedStepSize = 0
		Algorithm = 'dassl'
		"""
		self.run_cmd('experiment(StartTime=%s,StopTime=%s,OutputInterval=%s,NumberOfIntervals=%s,Tolerance=%s,FixedStepSize=%s,Algorithm="%s");'%(StartTime,StopTime,OutputInterval,NumberOfIntervals,Tolerance,FixedStepSize,Algorithm))
		self.run_cmd('simulate();')
		
	def set_parameters(self,pardict):
		"""
		sets all values in the parameter dictionary to their value
		"""
		for key,val in pardict.iteritems():
			try:
				self.run_cmd( '%s=%s'%(key,val) )
			except:
				print( 'could not assign %s to %s'%(key,val) )
				
	def get_result(self):
		"""
		loads results into a dictionary
		"""

		fileName = 'dsres.mat'
		fullFileName = os.path.abspath(fileName)

		fileData = scipy.io.loadmat(fullFileName, matlab_compatible=True)

		name = fileData["name"].T
		description = fileData["description"].T
		dataInfo = fileData["dataInfo"].T
		data_1 = fileData["data_1"]
		data_2 = fileData["data_2"]

		namelist = []
		for item in name:
			namelist.append(str(string.rstrip(string.join([x for x in item if len(x) > 0 and ord(x) < 128], ""))))

		name = namelist
		
		res = {}
		for idx,item in enumerate(name):
			if dataInfo[idx,0] == 1:
				# create a linspace  vector with the same length as data
				res[item] = scipy.sign(dataInfo[idx,1]) * scipy.linspace(data_1[abs(dataInfo[idx,1])-1][0], data_1[abs(dataInfo[idx,1])-1][1], len(data_2[0]) ) 
			else:
				res[item] = scipy.sign(dataInfo[idx,1]) * data_2[abs(dataInfo[idx,1])-1]
		
		return res
		
		