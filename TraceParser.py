#!/usr/bin/env python

from Node import Node

class TraceParser:
	def __init__(self):
		self.nodes = []

	def parse(self, f):
		for line in f:
			if line.startswith('M '):
				n = Node()
				n.read_line(line)
				self.nodes.append(n)
			else:
				break
