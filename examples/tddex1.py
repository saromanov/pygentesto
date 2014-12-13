import unittest
import random
import sys

#Unittest to classes

#From article TDD in python 5 minuts
#http://css.dzone.com/articles/tdd-python-5-minutes


#Output .py file with two classes or two different files with this classes
class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = list(range(0,10))

    def test_shuffle(self):
        # make sure the shuffled sequence does not lose any elements
        self.assertEqual(self.seq, list(range(0,10)))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def test_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)

class AnotherTest(unittest.TestCase):
    def setUp(self):
        self.data = ['first', 'word', 'ever']

    def test_length(self):
        self.assertEqual(len(self.data),3)

class TestAnother(unittest.TestLoader):
	def test_one(self):
		lst = [1,2,3,4]
		self.assertEqual(lst, [1,2,3,4])
if __name__ == '__main__':
    unittest.main()