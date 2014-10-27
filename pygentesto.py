import gentests
import tdd

import argparse
import json


def runGentests(path,outfile):

	gen = gentests.GenTests(path[0])
	gen.output(outfile)

def runGenTestsMany(paths):
	'''
		Construct unittest file/files
		from several .py files
	'''
	pass

def runTDD(path):
	inpfile, outfile = inpotp(path)
	t = tdd.TDD()
	t.parse(inpfile)
	t.output(outfile)


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
	args = parser.parse_args()
	if args.tdd != None:
		runTDD(args.tdd)
	if args.gentests != None:
		runGentests(args.gentests, args.output)
	if args.genstetsnum != None:
		"""
			Set every test num times
		"""
		num = int(args.genstetsnum[0])
		path = args.genstetsnum[1]



if __name__ == '__main__':
	parseArguments()