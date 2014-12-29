import re
import os
import ast
import json

from messages import Messages
from genoutput import ConstructPyFile
from util import TddOutput, ErrorOutput

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

	Configuration can be for all classes or methdos and individual configuration

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
		validmethdos = ['setUp']
		data = open(filename, 'r').read()
		tree = ast.parse(data)
		result = {}
		imported = []
		#Create objects for 
		objects = {}
		for node in ast.walk(tree):
			if isinstance(node, ast.ClassDef):
				#If function with same name exist - report the message
				self._check_exist_function(node.name, result)
				result[node.name] = []
				for subdata in node.body:
					if isinstance(subdata, ast.FunctionDef):
						funcs = result[node.name]
						#If function name not in fucs store with known functions
						if subdata.name not in funcs:
							cand_func = self._parse_test_function(subdata.name)
							#if cand_func return None
							#It is function from unittest
							if cand_func != None:
								result[node.name].append(cand_func)
							elif isinstance(subdata, ast.Assign):
								#In case with one function
								objects[subdata.body[0].targets[0].attr] = {'name':\
								subdata.body[0].value.func.id}
							elif subdata.name not in validmethdos:
								self.messages.error("During process of generation file, found error. Not valid TestCase file. method names should looks like test_name.",1)
								return ErrorOutput("Some error")
						else:
							self.messages.output("function {0} already exist in class {1}. Second function will not be generated.".\
								format(subdata.name, node.name))
						'''
							Parsing inside function to get expressions for create 
							classes and methods In the generated file
						'''
						objects.update(self._parse_inside_function(subdata.body, objects))
					if isinstance(subdata, ast.Expr):
						print("Some expression", subdata.value.s)
			if isinstance(node, ast.Import):
				imported += list(map(lambda x: 'import ' + x.name, node.names))
		return TddOutput(objects, imported, result)

	def _check_exist_function(self, funcname, store):
		if funcname in store:
			self.messages.output("function {0} already exist in store. New function with same name will be overwritten".\
				format(funcname))

	def _parse_test_function(self, name):
		""" Parse test function for getting clean name
			For example: test_one; return one

			return:
			objects - found objects in TestCase class
			imported - imported modeuls(need to move to objects)
			data - parse data from ast tree
		"""
		if name.startswith('test'):
			splitter = name.split('test')[1][1:]
			if splitter[1] =='':
				self.messages.output("function {0} have a empty name")
				return 'test'
			else: return splitter

	def _parse_inside_function(self, funcbody, objects):
		for body in funcbody:
			if isinstance(body, ast.Expr):
				for inner in body.value.args:
					if isinstance(inner, ast.Call):
						if isinstance(inner.func, ast.Attribute):
							name = inner.func.value.attr
							#Количество аргументов для функции
							number_of_args = len(inner.args)
							funcobj = FunctionObject(inner.func.attr, number_of_args)
							objects.update(self._update_arguments(name, funcobj, 'funcs', objects))
						if isinstance(inner.func, ast.Name):
							""" Case, where we have only function, without declaration in class
								For example: self.assertEqual(compute(5,10), 15)
							"""
							objects.update(self._update_arguments(' ', inner.func.id, 'funcs', objects))
		return objects

	def _update_arguments(self, name, data, param, objects):
		""" Update arguments for objects """
		if name in objects:
			if param in objects[name]:
				objects[name][param].append(data)
			else:
				objects[name].update({param: [data]})
		else:
			objects[name] = {'name': name, param:[data]}
		return objects

	def append_comments(self, subdata):
		"Append comments to file"
		if self.comments:
			return subdata.value.s


	#name - folder for output
	#newfiles - New file for every class
	def output(self, targetpath, outpath=None):
		#imported, data = self.parse(targetpath)
		result = self.ast_parse(targetpath)
		if not isinstance(result, TddOutput):
			return 
		objects = result.objects
		imported = result.imported
		data = result.data
		if self.construct:
			#TODO: append number arguments of function
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

	#All class in one file
	def _monoliticFile(self, value, outpath=None):
		data, result = value
		firstclassname = outpath
		if outpath == None:
			firstclassname = list(result.keys())[0]
			firstclassname = firstclassname.lower() + '.py'
		f = self._openFile(firstclassname)
		for d in data:
			f.write(d)
		f.close()
		self._writeData(result, firstclassname)

	def _openFile(self, path):
		""" Check if file exist
			Return his descriptior
		"""
		mode = 'a'
		if(os.path.isfile(path)):
			mode = 'w'
		return open(path, mode)

	def _writeData(self, result, path):
		"""
			result - object with map format to write in .py file
		"""
		f = self._openFile(path)
		[f.write(result[cls] + '\n') for cls in result.keys()]
		f.close()


class EmptyResultError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


class FunctionObject:
	""" Object from TestCase class
	"""
	def __init__(self, name, num_args):
		""" 
			name - Name of function
			num_args - number of arguments
		"""
		self.name = name
		self.num_args = num_args