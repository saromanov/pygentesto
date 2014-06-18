import gentests
import tdd
from genoutput import ConstructUnitTests

import argparse

def inpotp(path):
	return path[0], path[1]

def runGentests(path):
	inpfile, outfile = inpotp(path)
	gen = gentests.GenTests(inpfile)
	c = ConstructUnitTests(gen.result())
	c.output(outfile)

def runTDD(path):
	inpfile, outfile = inpotp(path)
	t = tdd.TDD()
	t.parse(inpfile)
	t.output(outfile)

def parseArguments():
	parser = argparse.ArgumentParser(description="Some parser")
	parser.add_argument('-g', dest="gentests", action='store', nargs='+', 
		help='Parse .py file and create tests')
	parser.add_argument('--tdd', dest='tdd', nargs='+',
		help='Create .py files after definition of tests')
	parser.add_argument('--diff-files', help='Store each сlass for different file')
	args = parser.parse_args()
	if args.tdd != None:
		runTDD(args.tdd)
	if args.gentests != None:
		runGentests(args.gentests)



if __name__ == '__main__':
	parseArguments()