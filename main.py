#!/usr/bin/env python

import sys
from MONA import MONA

def main(file):
	mona = MONA(file)
	mona.main()

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Usage: mona TRACEFILE"
		sys.exit()
	main(sys.argv[1])
