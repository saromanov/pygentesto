
class Messages:
	def __init__(self, isoutput):
		""" Class for output messages durning run of functions of generations
			isoutput - True|False - output message function
		"""
		self.isoutput = isoutput

	def output(self, message):
		if self.isoutput:
			self._report("Information ", message,5)
	def error(self, message, number):
		"""Message - Error message
		   numer - personal number of error
		"""
		self._report("Error ", message, number)

	def _report(self, level, message, number):
		print("{0}{1}: {2}".format(level, number, message))