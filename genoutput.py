import functools

class ConstructUnitTests:
	def __init__(self, classes):
		self.data = classes
		self.result = ''
		self.result += 'import unittest\n'
		self.params={}
		if imported != []:
			self.result += self._setImportData(imported)

	def add_class_for_each_method(self):
		self.params['cfem'] = '\t{0} = {1}()\n'

	def add_comment_for_method(self, comment):
		pass

	def appendImport(self, filename):
		""" TODO: Now, import from current path. Check unusual cases"""
		self.result += 'import {0}\n\n'.format(filename[0:filename.find('.')])

	def add_class_for_each_ut(self):
		'''
			Append class initialization for each unit test class
		'''
		self.params['cfeu'] = '\t{0} = {1}()\n'

	def _appendData(self, key, *data):
		if key in self.params:
			return self.params[key].format(*data)

	def _repeatFunc(self, data, times=1):
		#if times == 1:
		#	return '\tdef test_{0}(self):\n\t\tpass\n\n\n\n'.format(method)
		for step in range(times):
			for method in data:
				self.result += '\tdef test_{0}_{1}(self):\n\t\tpass\n\n\n\n'.format(method, step)
	def _writeData(self):
		for cls in self.data.keys():
			self.result += 'class Test{0}(unittest.TestCase):\n'.format(cls)
			#self.result += self._appendData('cfeu', cls[0], cls)
			'''if self.cfeu:
				self.result += '\t{0} = {1}()\n'.format(cls[0].lower(), cls)'''
			for method in self.data[cls]:
				self.result += '\tdef test_{0}(self):\n\t\tpass\n\n\n\n'.format(method)

	def _writeDataWComments(self):
		for cls in self.data.keys():
			self.result += 'class Test{0}(unittest.TestCase):\n'.format(cls)
			for method in self.data[cls]:
				name, comment = method
				self.result += '\tdef test_{0}(self):\n\t\t"""{1}"""\n\t\tpass\n\n\n\n'.format(name, comment)

	def _setMainData(self):
		self.result += '\n\n\nif __name__ == "__main__":\n\tunitest.main()\n'

	def _writeFile(self, outputfile):
		f = open(outputfile, 'w')
		f.write(self.result)

	def output(self, outputfile):
		self._writeData()
		self._setMainData()
		self._writeFile(outputfile)

	def output2(self, outputfile):
		""" Output with comments """
		self._writeDataWComments()
		self._setMainData()
		self._writeFile(outputfile)


class ConstructPyFile:
	'''
	Construct output file
	'''
	def __init__(self, path, data, imported=[]):
		self.path = path
		self.data = data
		self.result=''
		if imported != []:
			self.result += self._setImportData(imported)

	def _setImportData(self, imported):
		""" Set in file imported values"""
		imported = list(map(lambda x: x + '\n', imported))
		return functools.reduce(str.__add__, imported,'')

	def construct(self, istest=False):
		others = [self.result]
		result = {}
		class_string, method_string = self._makeData(istest)
		for cls in self.data.keys():
			data=''
			data += class_string.format(cls)
			result[cls] = ''
			for method in self.data[cls]:
				data += method_string.format(method)
			result[cls] = data
		return others, result

	def _makeData(self, istest=False):
		class_string = 'class {0}:\n'
		method_string = '\tdef {0}(self):\n\t\tpass\n'
		if istest:
			class_string = 'class {0}(unittest.TestCase):\n'
			method_string = '\tdef test_{0}(self):\n\t\tpass\n'
		return class_string, method_string