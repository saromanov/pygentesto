import gentests
import tdd

import argparse
import json


def runGentests(path,outfile,args):

	gen = gentests.GenTests(path[0])
	gen.output(outfile, imp=args.imp != None)

def runGenTestsMany(paths):
	'''
		Construct unittest file/files
		from several .py files
	'''
	pass

#python3.3 ../pygentesto.py --tdd ../examples/tddex2.py --output fun1.py
def runTDD(path, outpath, args):
	if path != None and outpath != None:
		""" 
			In case with inpath and outpath
		"""
		conf = args.configure
		t = tdd.Tdd(construct=args.construct, comments=args.comments, configure=conf)
		t.output(path, outpath=outpath)
	elif path != None:
		t = tdd.Tdd()
		t.output(path[0])


def confLoad():
	'''
		Load configuration
		repeatfunc - repeat number of times every function
	'''
	data = json.loads(open('conf.json').read())
	if repeatfunc in data:
		pass

#python3.3 pygentesto.py  -g pygentesto.py --output value.py
def parseArguments():
	parser = argparse.ArgumentParser(description="Some parser")
	parser.add_argument('-g', dest="gentests", action='store', nargs='+', 
		help='Parse .py file and create tests')
	parser.add_argument('--gN', dest="genstetsnum", action='store', nargs='+')
	parser.add_argument('--tdd', dest='tdd', nargs='+',
		help='Create .py files after definition of tests')
	parser.add_argument('--diff-files', help='Store each сlass for different file')
	parser.add_argument('--ci', dest='ci', help='class init for each test case', 
		const='ci', action='store_const')
	parser.add_argument('--cim', dest='cim', help='class init for each method',
		const='cim', action='store_const')
	parser.add_argument('--output', nargs='?', help='set output file')
	parser.add_argument('-i', dest='imp', help='import current file')

	#tdd keys
	parser.add_argument('--construct', dest='construct', nargs='+',
		help='Construct methods from TestCase class')
	parser.add_argument('--configure', dest='configure', nargs='+',
		help='Load all configuration from json file. Not need to use commad line keys')
	parser.add_argument('--comments', dest='comments', nargs='+', help='Append comments to output data')
	args = parser.parse_args()
	if args.tdd != None:
		runTDD(args.tdd, args.output, args)
	if args.gentests != None:
		runGentests(args.gentests, args.output, args)
	if args.genstetsnum != None:
		"""
			Set every test num times
		"""
		num = int(args.genstetsnum[0])
		path = args.genstetsnum[1]



if __name__ == '__main__':
	parseArguments()