#!/usr/bin/env python

from Node import Node
from Packet import Packet

class TraceParser:
	def __init__(self):
		self.nodes = {}
		self.packet_types = set()
		self.progress = 0.0

	def get_nodes(self):
		return self.nodes.values()

	def get_node(self, id):
		if not self.nodes.has_key(id):
			self.nodes[id] = Node()
		return self.nodes[id]

	def parse(self, f):
		lines        = f.readlines()
		inc_progress = 1.0 / len(lines)

		for line in lines:
			if line.startswith('M '):
				id = int(line.split()[2])
				self.get_node(id).read_line(line)
			else:
				event_type = line[0]

				if event_type in ['s', 'r', 'd', 'f']:
					packet = Packet(line)
					node   = self.get_node(packet.node_id)
					self.packet_types.add(packet.type)

					if event_type == 'r':
						node.receive_packet(packet)
					elif event_type == 's':
						node.send_packet(packet)

			self.progress += inc_progress

		self.progress = 1.0
