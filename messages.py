
class Messages:
	def __init__(self, isoutput):
		""" Class for output messages durning run of functions of generations
			isoutput - True|False - output message function
		"""
		self.isoutput = isoutput

	def output(self, message):
		if self.isoutput:
			print("Information: ", message)