#!/usr/bin/env python

import sys
from NAMM import NAMM
from TraceParser import TraceParser

def main(file):
	parser = TraceParser()

	f = open(file)
	parser.parse(f)
	f.close()

	namm = NAMM()
	namm.set_nodes(parser.get_nodes())
	namm.main()

if __name__ == '__main__':
	main(sys.argv[1])
