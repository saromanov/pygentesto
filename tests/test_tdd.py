import sys
sys.path.append("../")
from genoutput import ConstructPyFile
from tdd import Tdd

def test_tdd():
	tdd = Tdd()
	names = tdd.parse('../examples/tddex1.py')
	tdd.output('/', names)

test_tdd()