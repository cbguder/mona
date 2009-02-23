#!/usr/bin/env python

import sys
from MONA import MONA
from TraceParser import TraceParser

def main(file):
	parser = TraceParser()

	f = open(file)
	parser.parse(f)
	f.close()

	mona = MONA()
	mona.set_nodes(parser.get_nodes())
	mona.main()

if __name__ == '__main__':
	main(sys.argv[1])
