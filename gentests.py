import inspect
import os.path
import re
from genoutput import ConstructUnitTests

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
3. Fix bug with check def and class in comments
'''

class GenTests:
	'''
	GenTests('filename')

	'''
	def __init__(self, fname=__file__, *args, **kwargs):

		#Filename or filenames
		self.fname = fname
		self.closed_methods = kwargs.get('closed', False)
		self.classinit_store = kwargs.get('classinit', True)
		self.classinit_method = kwargs.get('classmethod', False)

		#By default - generate tests for all public methods
		self.genall = kwargs.get('genall', True)
		if not self.genall:
			self.methods = {}
		self.defaultClass = 'TEST'
		#Classes like a dictionary
		#self.classes=self._getClassNames()

	def _getClassNames(self):
		"""
			Get all class names in .py file
			return: list of all class names
			In case, when file not contain classes - empty list
		"""
		return self._getNames('^class \w+')

	def _readFile(self, path):
		"""
			Read source file if exist
		"""
		assert(os.path.isfile(path))
		return open(self.fname, 'r').readlines()
	def _getNames(self, pattern):
		"""
			Get classes and functions
			TODO: Need rewrite with ast
		"""
		data = self._readFile(self.fname)
		store = Store(self.fname)
		self.searchClasses(data)
		startposclass = 99999999
		for i in data:
			data = re.search(pattern,i)
			if data != None:
				startposclass = len(i)
				result = data.group(0).split()
				store.appendClass(result)
			data2 = re.search('def \w+', i)
			if data2 != None:
				'''Check distance between class(c) name and def(d) function
				if c > d then dеf is method of c
				otherwise is a function which not contaon in c
				'''
				if startposclass < len(i):
					result = data2.group(0).split()
					store.appendMethodToClass(result)
				else:
					result = data2.group(0).split()
					store.appendMethod(result)
		newDict = {}
		values = store.getValues()
		if len(values) > 0:
			return {keys: self._filterNames(values[keys]) for keys in values.keys()}
		else:
			return store.getMethods()

	def searchClasses(self, data):
		'''
			If file not contain any class, construct
			only with function with filename as testcase class
		'''
		pass

	#Filter method names
	def _filterNames(self, names):
		if self.closed_methods == False:
			return list(filter(lambda x: x.startswith("_") == False, names))
		return names

	def parse(self):
		return self._getNames(pattern)

	def generate(self, methodname, comment):
		"""
			Generate addition test case for the method
			For example:
			gen = GenTests(genall=False)
			gen.generate('example3', 'value if out of range')
			output:
			def test_example3(self):
				'value is out of range'
				pass

			TODO: Need to append comment
		"""
		if self.genall == False:
			if self.defaultClass not in self.methods:
				self.methods[self.defaultClass] = [(methodname, comment)]
			else:
				self.methods[self.defaultClass].append((methodname, comment))

	def addDefaultClass(self, classname):
		self.defaultClass = classname


	def choosenMethods(self):
		"""
			Generate only with choosen methods
		"""
		pass

	def _getMethodNames(self):
		pass

	def _checkfile(self):
		pass

	def _result(self):
		"""
			Return dict with class names and list of methods
		"""
		if self.genall:
			classes = self._getClassNames()
			return classes
		else: return self.methods

	def output(self, path, *args, **kwargs):
		result = self._result()
		classes_w_methods = {cl:result[cl] for cl in result if len(result[cl]) > 0}
		c = ConstructUnitTests(classes_w_methods)
		if self.classinit_store:
			c.add_class_for_each_ut()
		if self.classinit_method:
			c.add_class_for_each_method()
		if kwargs.get('imp'):
			c.appendImport(self.fname)
		if self.genall:
			return c.output(path)
		else:
			return c.output2(path)



class Store:
	def __init__(self,path):
		self.class_names=[]
		self.method_names=[]
		self.values = {}
		self.path = path.split('.')[0]

	def appendClass(self, classname):
		self.class_names.append(classname[1])
		if classname[1] not in self.values:
			self.values[classname[1]] = []

	def appendMethod(self, methodname):
		if methodname[1] not in self.method_names:
			self.method_names.append(methodname[1])

	def appendMethodToClass(self, methodname):
		self.method_names.append(methodname[1])
		if self.class_names[-1] in self.values:
			self.values[self.class_names[-1]].append(methodname[1])

	def getValues(self):
		return self.values

	def getMethods(self):
		return {self.path: self.method_names}

