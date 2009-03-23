#!/usr/bin/env python

from Point import Point

class Node:
	def __init__(self):
		self.movements = []
		self.packets   = []
		self.active    = False
		self.first_activity = None

	def read_line(self, line):
		m = NodeMovement()
		m.load_trace(line)
		self.movements.append(m)

	def position_at(self, time):
		movement = None
		for m in self.movements:
			if m.src_time > time:
				break
			movement = m

		if movement == None:
			return None
		else:
			return movement.position_at(time)

	def active_at(self, time):
		return self.first_activity != None and time >= self.first_activity

	def receive_packet(self, packet):
#		self.packets.append(packet)
		if self.first_activity == None and packet.type == 'VirtualSign':
			self.first_activity = packet.time

	def send_packet(self, packet):
#		self.packets.append(packet)
		if self.first_activity == None and packet.type == 'VirtualSign':
			self.first_activity = packet.time

class NodeMovement:
	def __init__(self):
		self.src        = Point()
		self.dest       = Point()
		self.src_time   = 0.0
		self.speed      = 0.0
		self.distance   = 0.0
		self.total_time = 0.0
		self.dx         = 0.0
		self.dy         = 0.0

	def load_trace(self, trace):
		l = trace.split()
		self.src_time   = float(l[1])
		self.src.x      = float(l[3][1:-1])
		self.src.y      = float(l[4][:-1])
		self.src.z      = float(l[5][:-2])
		self.dest.x     = float(l[6][1:-1])
		self.dest.y     = float(l[7][:-2])
		self.speed      = float(l[8])

		self.distance   = self.src.distance_to(self.dest)
		self.total_time = self.distance / self.speed
		self.dx         = self.dest.x - self.src.x
		self.dy         = self.dest.y - self.src.y

	def position_at(self, time):
		dt = time - self.src_time

		if dt > 0.0 and self.total_time > 0.0:
			ratio = dt / self.total_time 
			p = Point()
			p.x = self.src.x + self.dx * ratio
			p.y = self.src.y + self.dy * ratio
			return p
		else:
			return self.src

if __name__ == '__main__':
	n = Node()
	n.read_line('M 0.00000 0 (0.0, 0.0, 0.0), (100.0, 0.0), 20.0')
	n.read_line('M 5.00000 0 (100.0, 0.0, 0.0), (0.0, 0.0), 20.0')
	t = 0.0
	while t < 10:
		print 'AT %.1fs: %s' % (t, n.position_at(t))
		t += 1.0
