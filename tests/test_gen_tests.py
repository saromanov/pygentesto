import sys
sys.path.append("../")
from genoutput import ConstructUnitTests
from gentests import GenTests

def test_gentests():
	gen = GenTests('./methods.py')
	gen.output('simple.py')


def example2():
	gen = GenTests('./fundata.py')
	gen.output('simple.py')

def example3():
	gen = GenTests(genall=False)
	gen.addDefaultClass('Checker')
	values = list(range(10))
	arr = ['foo', 'bar']
	if len(values) < 20:
		gen.generate('example3', 'value is out of range')
	if 'data' not in arr:
		gen.generate('example4', 'data not contain arr')
	gen.output('simple.py')
