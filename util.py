
class TddOutput:
	"""
		Nice output from main function tdd
	"""
	def __init__(self, objects, imported, data):
		self.objects = objects
		self.imported = imported
		self.data = data


class ErrorOutput:
	def __init__(self, message):
		self.message = message