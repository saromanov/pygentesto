import unittest

class TestSettings2(unittest.TestCase):
	'''
		Test case with two identical functions
		Should generate one function with warning message
	'''
	def test_one(self):
		self.assertEqual(True, True)

	def test_one(self):
		self.assertEqual(True, True)

