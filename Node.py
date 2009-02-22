#!/usr/bin/env python

from Point import Point

class Node:
	def __init__(self):
#		self.id       = 0
		self.src      = Point()
		self.dest     = Point()
		self.src_time = 0.0
		self.speed    = 0.0
		self.distance = 0.0

	def read_line(self, line):
		l = line.split()
		self.src_time   = float(l[1])
#		self.id         = int(l[2])
		self.src.x      = float(l[3][1:-1])
		self.src.y      = float(l[4][:-1])
#		self.src.z      = float(l[5][:-2])
		self.dest.x     = float(l[6][1:-1])
		self.dest.y     = float(l[7][:-2])
		self.speed      = float(l[8])

		self.distance   = self.src.distance_to(self.dest)
		self.total_time = self.distance / self.speed
		self.dx         = self.dest.x - self.src.x
		self.dy         = self.dest.y - self.src.y

	def position_at(self, time):
		dt = time - self.src_time

		if dt > 0.0:
			ratio = dt / self.total_time 
			p = Point()
			p.x = self.src.x + self.dx * ratio
			p.y = self.src.y + self.dy * ratio
			return p
		else:
			return self.src

if __name__ == '__main__':
	n = Node()
	n.read_line('M 0.00000 0 (1474.03, 609.20, 0.00), (1514.98, 612.62), 13.69')
	print 'DISTANCE:', n.distance
	print 'TIME:    ', n.total_time
	print
	print 'SOURCE:  ', n.src
	print 'DEST.:   ', n.dest
	print
	t = 0.0
	while t < n.total_time:
		print 'AT %.1fs: %s' % (t, n.position_at(t))
		t += 1.0
