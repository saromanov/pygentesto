import unittest
import os
import numpy

'''class TestSettings2(unittest.TestCase):
	"""
		Test case with two identical functions
		Should generate one function with warning message
	"""
	def test_one(self):
		self.assertEqual(True, True)



class CoolWebService(unittest.TestCase):
	#Set first initialization
	def test_init(self):
		pass

	#Test to load data
	def test_load(self):
		pass
'''

class TestCalculator(unittest.TestCase):
	def setUp(self):
		self.calculator = Calculator()

	def test_multiply(self):
		self.assertEqual(self.calculator.multi(7,6), 42)

	def test_added(self):
		self.assertEqual(self.calculator.add(7,6), 13)

def raises_error(*args, **kwds):
    raise ValueError('Invalid value: %s%s' % (args, kwds))

class ExceptionTest(unittest.TestCase):

    def test_trap_locally(self):
        try:
            raises_error('a', b='c')
        except ValueError:
            pass
        else:
            self.fail('Did not see ValueError')

    def test_assert_raises(self):
        self.assertRaises(ValueError, raises_error, 'a', b='c')

if __name__ == '__main__':
	unittest.main()