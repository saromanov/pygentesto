import inspect
import os.path
import re


'''
Algorithm
1. Read .py file
2. Parse class names and name of methods
3. Create new file with unittests with these data
'''

'''
TODO:
1. docstring
2. ddt
'''

class GenTests:
	'''
	GenTests('filename')

	What about private methods?
	'''
	def __init__(self, fname, *args, **kwargs):
		self.fname = fname
		self.closed_methods = kwargs.get('closed', False)
		#Classes like a dictionary
		#self.classes=self._getClassNames()

	def _getClassNames(self):
		return self._getNames('class \w+')

	def _getNames(self, pattern):
		class_names = []
		method_names = []
		values = {}
		assert(os.path.isfile(self.fname))
		f = open(self.fname, 'r').readlines()
		for i in f:
			data = re.search(pattern,i)
			if data != None:
				result = data.group(0).split()
				class_names.append(result[1])
				if result[1] not in values:
					values[result[1]] = []
			data2 = re.search('def \w+', i)
			if data2 != None:
				result = data2.group(0).split()
				method_names.append(result[1])
				if class_names[-1] in values:
					values[class_names[-1]].append(result[1])
		newDict = {}
		for keys in values.keys():
			newDict[keys] = self._filterNames(values[keys])
		return newDict

	#Filter method names
	def _filterNames(self, names):
		if self.closed_methods == False:
			return list(filter(lambda x: x.startswith("_") == False, names))
		return names

	def parse(self):
		return self._getNames(pattern)

	def _getMethodNames(self):
		pass

	def _checkfile(self):
		pass

	def result(self):
		return self._getClassNames()
