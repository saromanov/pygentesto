import sys
sys.path.append("../")
from genoutput import ConstructPyFile
from tdd import Tdd

def test_tdd():
	tdd = Tdd()
	#names = tdd.parse('../examples/tddex1.py')
	tdd.output('../examples/tddex1.py', 'datapoor.py')

def test_tdd2():
	tdd = Tdd()
	tdd.output('../examples/tddex2.py')

test_tdd()