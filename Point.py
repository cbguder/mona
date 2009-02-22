#!/usr/bin/env python

from math import sqrt

class Point:
	def __init__(self):
		self.x = 0.0
		self.y = 0.0

	def distance_to(self, p):
		return sqrt((self.x - p.x)**2 + (self.y - p.y)**2)

	def __str__(self):
		return (self.x, self.y).__str__()
