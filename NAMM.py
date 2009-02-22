#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

NODE_SIZE = 4.0

from threading import Thread


class NAMM:
	def window_delete(self, widget, event, data=None):
		return False

	def window_destroy(self, widget, data=None):
		gtk.main_quit()

	def drawing_area_exposed(self, widget, data=None):
		self.draw()

	def draw(self):
		self.statusbar.push(0, '%.4f' % self.t)
		self.statusbar.queue_draw()

		rect = self.drawing_area.get_allocation()
		style = self.drawing_area.get_style()

		pos = [n.position_at(self.t) for n in self.nodes]

		self.drawing_area.window.draw_rectangle(style.bg_gc[gtk.STATE_NORMAL], True, 0, 0, rect.width, rect.height)
		for p in pos:
			self.drawing_area.window.draw_arc(style.fg_gc[gtk.STATE_NORMAL], True,
			                       rect.width  * (p.x / 2400.0) - NODE_SIZE/2,
			                       rect.height * (p.y / 2400.0) - NODE_SIZE/2,
			                       NODE_SIZE, NODE_SIZE,
			                       0, 64 * 360)

	def step(self):
		self.t += self.adjustment.value
		self.draw()

	def rewind_clicked(self, widget, data=None):
		self.t = 0.0
		self.draw()

	def play(self):
		while self.t < 100.0:
			gtk.gdk.threads_enter()
			self.step()
			gtk.gdk.threads_leave()

	def start_clicked(self, widget, data=None):
		th = Thread(target=self.play)
		th.start()

	def __init__(self):
		self.nodes = None
		self.t     = 0.0

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect('destroy', self.window_destroy)
		self.window.set_border_width(2)

		self.vbox = gtk.VBox(False, 10)
		self.window.add(self.vbox)

		self.hbox = gtk.HBox()
		self.vbox.pack_start(self.hbox, False, True)

		self.rewind = gtk.Button(None, gtk.STOCK_MEDIA_REWIND)
		self.rewind.connect('clicked', self.rewind_clicked)
		self.hbox.add(self.rewind)

		self.start = gtk.Button(None, gtk.STOCK_MEDIA_PLAY)
		self.start.connect('clicked', self.start_clicked)
		self.hbox.add(self.start)

		self.adjustment = gtk.Adjustment(0.1, 0.01, 1.0, 0.01, 0.1)
		self.spinbutton = gtk.SpinButton(self.adjustment, 0.01, 2)
		self.hbox.add(self.spinbutton)

		self.drawing_area = gtk.DrawingArea()
		self.drawing_area.connect('expose_event', self.drawing_area_exposed)
		self.drawing_area.set_size_request(512, 512)
		self.vbox.pack_start(self.drawing_area)

		self.statusbar = gtk.Statusbar()
		self.vbox.pack_end(self.statusbar, False, True)

		self.window.show_all()

	def main(self):
		gtk.gdk.threads_init()
		gtk.gdk.threads_enter()
		gtk.main()
		gtk.gdk.threads_leave()
