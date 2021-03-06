import sys
sys.path.append("../")
from genoutput import ConstructPyFile
from tdd import Tdd

def test_tdd():
	tdd = Tdd()
	#names = tdd.parse('../examples/tddex1.py')
	tdd.output('../examples/tddex1.py', 'datapoor.py')

def test_tdd2():
	tdd = Tdd(configure='conf.json')
	tdd.output('../examples/tddex2.py', outpath='day1.py')

def test_tdd3():
	tdd = Tdd(comments=False)
	tdd.output('../examples/tddex2.py', outpath='day1.py')

def test_ident_class_names():
	tdd = Tdd(ismessages=True)
	tdd.output('../examples/tddex3.py', outpath='day2.py')

#test_tdd3()
test_ident_class_names()