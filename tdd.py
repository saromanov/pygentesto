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
	configure - path to configuration json file
	'''
	def __init__(self, newclass=False, ismessages=False, comments=False, configure=None):
		if configure != None:
			pass
		self.newclass = newclass
		self.comments = comments
		self.messages = Messages(ismessages)

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
		print(objects, ...)
		return imported, result

	def _parse_test_function(self, name):
		""" Parse test function for getting clean name
			For example: test_one; return one
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