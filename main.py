#!/usr/bin/env python

import sys
from MONA import MONA
from TraceParser import TraceParser

def main(file):
	parser = TraceParser()

	try:
		f = open(file)
	except IOError, e:
		print "mona: cannot open %s: %s" % (file, e.args[1])
		sys.exit()
	parser.parse(f)
	f.close()

	mona = MONA()
	mona.set_nodes(parser.get_nodes())
	mona.main()

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Usage: mona TRACEFILE"
		sys.exit()
	main(sys.argv[1])
