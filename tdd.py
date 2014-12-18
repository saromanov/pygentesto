import re
import os
import ast
import json

from messages import Messages
from genoutput import ConstructPyFile

#Write tests and gen classes


class Tdd:
	'''
	path - 
	newclass - create new class with every new method
	messages - output information messages which occurred during process of generation .py file
	configure - path to configuration of json file

	configure:
	construct - construct classes from testCase class(with name of class. For example:

	[code]
	class TestCalculator(unittest.TestCase):
		def setUp(self):
			self.calculator = Calculator()

		def test_multiply(self):
			self.assertEqual(self.calculator.multi(7,6), 42)
	[/code]
	In output .py file will be class Calculator with method multi

	'''
	def __init__(self, newclass=False, ismessages=False, comments=False, configure=None,\
		construct=None):
		self.configure = None
		if configure != None:
			self.configure = self._load_configure(configure)
		else:
			self.newclass = newclass
			self.comments = comments
			self.messages = Messages(ismessages)
			self.construct = construct

	def _load_configure(self, path):
		if path != None:
			with open(path) as f:
				return json.loads(f.read())

	def ast_parse(self, filename):
		""" Parse classes with test cases and functions """
		if not os.path.isfile(filename):
			raise Exception("File not found")
		data = open(filename, 'r').read()
		tree = ast.parse(data)
		result = {}
		imported = []
		#Create objects for 
		objects = {}
		for node in ast.walk(tree):
			if isinstance(node, ast.ClassDef):
				result[node.name] = []
				for subdata in node.body:
					if isinstance(subdata, ast.FunctionDef):
						funcs = result[node.name]
						if subdata.name not in funcs:
							cand_func = self._parse_test_function(subdata.name)
							# if cand_func return None
							#It is function from unittest
							if cand_func != None:
								result[node.name].append(cand_func)
							else:
								#In case with one function
								objects[subdata.body[0].targets[0].attr] = {'name':\
								subdata.body[0].value.func.id}
						else:
							self.messages.output("function {0} already exist in class {1}. Second function will not be generated".\
								format(subdata.name, node.name))
						self._parse_inside_function(subdata.body, objects)
					if isinstance(subdata, ast.Expr):
						print("Something expression", subdata.value.s)
			if isinstance(node, ast.Import):
				imported = list(map(lambda x: 'import ' + x.name, node.names))
		return objects, imported, result

	def _parse_test_function(self, name):
		""" Parse test function for getting clean name
			For example: test_one; return one

			return:
			objects - found objects in TestCase class
			imported - imported modeuls(need to move to objects)
			data - parse data from ast tree
		"""
		if name.startswith('test'):
			splitter = name.split('_')
			if splitter[1] =='':
				self.messages.output("function {0} have a empty name")
				return 'test'
			else: return splitter[1]

	def _parse_inside_function(self, funcbody, objects):
		for body in funcbody:
			if isinstance(body, ast.Expr):
				for inner in body.value.args:
					if isinstance(inner, ast.Call):
						name = inner.func.value.attr
						if name in objects:
							if 'funcs' in objects[name]:
								objects[name]['funcs'].append(inner.func.attr)
							else:
								objects[name].update({'funcs': [inner.func.attr]})
		return objects

	def append_comments(self, subdata):
		"Append comments to file"
		if self.comments:
			return subdata.value.s


	#name - folder for output
	#newfiles - New file for every class
	def output(self, targetpath, outpath=None):
		#imported, data = self.parse(targetpath)
		objects, imported, data = self.ast_parse(targetpath)
		if self.construct:
			self._constructObjects(objects, outpath)
		else:
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

	def _constructObjects(self, objects, path):
		if objects == None:
			self.messages.output("objects from TestCase class not found")
			return
		for obj in objects.keys():
			construct = objects[obj]
			transform = {construct['name']: construct['funcs']}
			imported, output = ConstructPyFile(path, transform).construct()
			self._writeData(output, path)
			#print(output, ...)

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
		f.close()
		self._writeData(result, outpath)

	def _writeData(self, result, path):
		"""
			result - object with map format to write in .py file
		"""
		f = open(path, 'w')
		[f.write(result[cls] + '\n') for cls in result.keys()]
		f.close()


class EmptyResultError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)