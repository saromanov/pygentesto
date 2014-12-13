import re
from genoutput import ConstructPyFile
import os
from messages import Messages

#Write tests and gen classes


class Tdd:
	'''
	path - 
	newclass - create new class with every new method
	messages - output information messages which occurred during process of generation .py file
	'''
	def __init__(self, newclass=False, ismessages=False):
		self.newclass = newclass
		self.messages = Messages(ismessages)

	#TODO case when not classes in file
	def parse(self, filename):
		""" Parse .py test case file to construct 
		    another .py file with "clean" classes with function
		"""
		if not os.path.isfile(filename):
			raise Exception("File not exists")
		#Class and methods
		params = {}
		imported = []
		data = open(filename, 'r').readlines()
		for c in data:
			importvalue = re.search("import \w+", c)
			if importvalue != None:
				imported.append(importvalue.group(0))
			resultc = re.search("class \w+", c)
			foundclass=False
			if resultc != None:
				clname = resultc.group(0).split('Test')[1]
				if clname != '':
					params[clname] = []
			resultm = re.search("def \w+", c)
			if resultm != None:
				checksplit = resultm.group(0).split('test')
				if len(checksplit) > 1:
					mlname = resultm.group(0).split('test_')[1]
					if clname in params and mlname != '':
						storedfuncs = params[clname]
						if mlname in storedfuncs:
							self.messages.output("function {0} already exist in class {1}. Second function will not be generated".\
								format(mlname, clname))
						else:
							params[clname].append(mlname)
		return imported, params


	#name - folder for output
	#newfiles - New file for every class
	def output(self, targetpath, outpath=None):
		imported, data = self.parse(targetpath)
		otput = ConstructPyFile(outpath, data, imported=imported)
		result = otput.construct()
		if result == None:
			raise EmptyResultError("Result not contain any output")
		if self.newclass:
			self._alwaysNewFile(result)
		else:
			self._monoliticFile(result)

	#New file for every class
	def _alwaysNewFile(self, result):
		for cls in result.keys():
			f = open(cls.lower() + '.py', 'w')
			f.write(result[cls])

	#All class in one file
	def _monoliticFile(self, value):
		data, result = value
		firstclassname = list(result.keys())[0]
		f = open(firstclassname.lower() + '.py', 'w')
		for d in data:
			f.write(d)
		for cls in result.keys():
			f.write(result[cls])

class EmptyResultError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)