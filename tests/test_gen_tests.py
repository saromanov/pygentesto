import sys
sys.path.append("../")
from genoutput import ConstructUnitTests
from gentests import GenTests

def test_gentests():
	gen = GenTests('../gentests.py')
	c = ConstructUnitTests(gen.result())
	c.output('test_gentests.py')

test_gentests()