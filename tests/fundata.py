
#File with classes

class FunData:
	"""
		This is example class
	"""

	def __init__(self, value):
		self.value = value

	def compute1(self, another):
		return sum(list(map(lambda x: (x[0] - x[1])**2, zip(self.value, another))))

	def compute2(self, another):
		return list(map(lambda x: (x[0] - x[1])**2, zip(self.value, another)))