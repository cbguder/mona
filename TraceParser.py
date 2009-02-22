#!/usr/bin/env python

from Node import Node

class TraceParser:
	def __init__(self):
		self.nodes = {}

	def get_nodes(self):
		return self.nodes.values()

	def parse(self, f):
		for line in f:
			if line.startswith('M '):
				id = int(line.split()[2])
				if not self.nodes.has_key(id):
					self.nodes[id] = Node()
				self.nodes[id].read_line(line)
