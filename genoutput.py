class ConstructUnitTests:
	def __init__(self, classes):
		self.data = classes
		self.result = ''
		self.result += 'import unittest\n'
		self._writeData()

	def _writeData(self):
		for cls in self.data.keys():
			self.result += 'class {0}(unittest.TestCase):\n'.format(cls)
			for method in self.data[cls]:
				self.result += '\tdef test_{0}(self):\n\t\tpass\n'.format(method)

	def output(self, outputfile):
		ct = ConstructUnitTests(self.data)
		f = open(outputfile, 'w')
		f.write(self.result)


class ConstructPyFile:
	'''
	Construct output file
	'''
	def __init__(self, path, data):
		self.path = path
		self.data = data

	def construct(self, istest=False):
		result = {}
		class_string, method_string = self._makeData(istest)
		for cls in self.data.keys():
			data=''
			data += class_string.format(cls)
			result[cls] = ''
			for method in self.data[cls]:
				data += method_string.format(method)
			result[cls] = data
		return result

	def _makeData(self, istest=False):
		class_string = 'class {0}:\n'
		method_string = '\tdef {0}(self):\n\t\tpass\n'
		if istest:
			class_string = 'class {0}(unittest.TestCase):\n'
			method_string = '\tdef test_{0}(self):\n\t\tpass\n'
		return class_string, method_string