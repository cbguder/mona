#!/usr/bin/env python

from Node import Node

class TraceParser:
	def __init__(self):
		self.nodes = {}
		self.packet_types = set()
		self.progress = 0.0

	def get_nodes(self):
		return self.nodes.values()

	def parse(self, f):
		lines        = f.readlines()
		inc_progress = 1.0 / len(lines)

		for line in lines:
			if line.startswith('M '):
				id = int(line.split()[2])
				if not self.nodes.has_key(id):
					self.nodes[id] = Node()
				self.nodes[id].read_line(line)
			elif line[0] in ['s', 'r']:
				packet = parse_packet(line)
				self.packet_types.add(packet['It'])

			self.progress += inc_progress

		self.progress = 1.0

def parse_packet(line):
	packet = {}
	parts  = line.split()
	packet['type'] = parts[0]

	for i in range(len(parts))[1::2]:
		packet[parts[i][1:]] = parts[i+1]

	packet['If'] = int(packet['Ii'])
	packet['Ii'] = int(packet['Ii'])
	packet['Ni'] = int(packet['Ni'])

	return packet
