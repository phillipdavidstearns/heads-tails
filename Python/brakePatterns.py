#!/usr/local/bin/python3
import sys
from time import *

counter = 0

#------------------------------------------------------------------------

class Driver:

	seqs, ptrns = (0, 0)
	brkPtrns = [[0 for col in range(ptrns)] for row in range(seqs)] 

	def __init__(self,
		_seqs=0,
		_ptrns=0,
		_ID=0,
		_brkDel=0,
		_brkDelVar=0,
		_brkDur=0,
		_brkDurVar=0,
		_relDel=0,
		_relDelVar=0):
		seqs, ptrns = (_seqs, _ptrns)
		brkPtrns = [[0 for col in range(ptrns)] for row in range(seqs)]
		
	def printPtrns(self):
		print("We made it!")
		print(brkPtrns)

#------------------------------------------------------------------------

def main():
	global counter
	print("Main code here!")
	counter = counter + 1
	if counter > 5:
		d = Driver()
		d.printPtrns()
		sys.exit(0)

#------------------------------------------------------------------------

while True:
	main()
	sleep(.01)
