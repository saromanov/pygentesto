import sys
sys.path.append("../")
from genoutput import ConstructUnitTests
from gentests import GenTests

def test_gentests():
	gen = GenTests('./methods.py')
	gen.output('simple.py')


def example2():
	gen = GenTests('./fundata.py')
	#Set number of cases
	#gen.tests('')
	gen.output('simple.py')

def example3():
	gen = GenTests(genall=False)
	values = list(range(10))
	if len(values) < 20:
		gen.generate('example3')
	gen.output('simple')

