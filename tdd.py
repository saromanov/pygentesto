import re
from genoutput import ConstructPyFile
import os
from messages import Messages
import ast

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

	def ast_parse(self, filename):
		""" Parse classes with test cases and functions """
		if not os.path.isfile(filename):
			raise Exception("File not found")
		data = open(filename, 'r').read()
		tree = ast.parse(data)
		result = {}
		imported = []
		for node in ast.walk(tree):
			if isinstance(node, ast.ClassDef):
				result[node.name] = []
				for subdata in node.body:
					if isinstance(subdata, ast.FunctionDef):
						funcs = result[node.name]
						if subdata.name not in funcs:
							result[node.name].append(subdata.name)
						else:
							self.messages.output("function {0} already exist in class {1}. Second function will not be generated".\
								format(subdata.name, node.name))
					if isinstance(subdata, ast.Expr):
						print("Something expression", subdata.value.s)
			if isinstance(node, ast.Import):
				imported = list(map(lambda x: 'import ' + x.name, node.names))
		return imported, result


	#name - folder for output
	#newfiles - New file for every class
	def output(self, targetpath, outpath=None):
		#imported, data = self.parse(targetpath)
		imported, data = self.ast_parse(targetpath)
		otput = ConstructPyFile(outpath, data, imported=imported)
		result = otput.construct()
		if result == None:
			raise EmptyResultError("Result not contain any output")
		if self.newclass:
			self._alwaysNewFile(result)
		else:
			self._monoliticFile(result, outpath=outpath)

	#New file for every class
	def _alwaysNewFile(self, result):
		for cls in result.keys():
			f = open(cls.lower() + '.py', 'w')
			f.write(result[cls])

	#All class in one file
	def _monoliticFile(self, value, outpath=None):
		data, result = value
		firstclassname = outpath
		if outpath == None:
			firstclassname = list(result.keys())[0]
			firstclassname = firstclassname.lower() + '.py'
		f = open(firstclassname, 'w')
		for d in data:
			f.write(d)
		for cls in result.keys():
			f.write(result[cls] + '\n')

class EmptyResultError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)