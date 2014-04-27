import re
from genoutput import ConstructPyFile
import os

#Write tests and gen classes


class Tdd:
	'''
	path - 
	newclass - create new class with every new method
	'''
	def __init__(self, newclass=False):
		self.newclass = newclass

	#TODO case when not classes in file
	def parse(self, filename):
		if not os.path.isfile(filename):
			raise Exception("File not exists")
		#Class and methods
		params = {}
		data = open(filename, 'r').readlines()
		for c in data:
			resultc = re.search("class \w+", c)
			if resultc != None:
				clname = resultc.group(0).split('Test')[1]
				params[clname] = []
			resultm = re.search("def \w+", c)
			if resultm != None:
				checksplit = resultm.group(0).split('test')
				if len(checksplit) > 1:
					mlname = resultm.group(0).split('test_')[1]
					params[clname].append(mlname)
		return params


	#name - folder for output
	#newfiles - New file for every class
	def output(self, path, data):
		otput = ConstructPyFile(path, data)
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
	def _monoliticFile(self, result):
		firstclassname = list(result.keys())[0]
		f = open(firstclassname.lower() + '.py', 'w')
		for cls in result.keys():
			f.write(result[cls])

class EmptyResultError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)