#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

gtk.gdk.threads_init()

NODE_SIZE = 4

import time
from threading import Thread

class MONA:
	def window_delete(self, widget, event, data=None):
		return False

	def window_destroy(self, widget, data=None):
		gtk.main_quit()

	def draw(self):
		self.statusbar.push(0, '%.2f' % self.t)
		self.statusbar.queue_draw()

		rect = self.image.get_allocation()
		style = self.image.get_style()

		self.pos = [n.position_at(self.t) for n in self.nodes]

		pixmap = gtk.gdk.Pixmap(None, rect.width, rect.height, 24)
		pixmap.draw_rectangle(style.bg_gc[gtk.STATE_NORMAL], True, 0, 0, rect.width, rect.height)
		for p in self.pos:
			pixmap.draw_arc(style.fg_gc[gtk.STATE_NORMAL], True,
			                int(rect.width  * (p.x / 2400.0) - NODE_SIZE/2),
			                int(rect.height * (p.y / 2400.0) - NODE_SIZE/2),
			                NODE_SIZE, NODE_SIZE,
			                0, 64 * 360)

		self.image.set_from_pixmap(pixmap, None)

	def step(self):
		self.t += self.adjustment.value
		self.draw()

	def rewind_clicked(self, widget, data=None):
		self.fstop = True
		self.t = 0.0
		self.draw()

	def play(self):
		while self.t < 100 and not self.fstop:
			gtk.gdk.threads_enter()
			self.step()
			gtk.gdk.threads_leave()
			time.sleep(0.005)
		self.start.set_sensitive(True)
		self.stop.set_sensitive(False)

	def start_clicked(self, widget, data=None):
		self.fstop = False
		self.stop.set_sensitive(True)
		widget.set_sensitive(False)
		th = Thread(target=self.play)
		th.start()

	def stop_clicked(self, widget, data=None):
		self.fstop = True
		widget.set_sensitive(False)

	def __init__(self):
		self.nodes = None
		self.t     = 0.0
		self.pos   = None
		self.fstop = False

		self.window = gtk.Window()
		self.window.connect('destroy', self.window_destroy)
		self.window.set_border_width(2)
		self.window.set_title('MONA')

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

		self.stop = gtk.Button(None, gtk.STOCK_MEDIA_STOP)
		self.stop.connect('clicked', self.stop_clicked)
		self.stop.set_sensitive(False)
		self.hbox.add(self.stop)

		self.adjustment = gtk.Adjustment(0.1, 0.01, 1.0, 0.01, 0.1)
		self.spinbutton = gtk.SpinButton(self.adjustment, 0.01, 2)
		self.hbox.add(self.spinbutton)

		self.image = gtk.Image()
		self.image.set_size_request(512, 512)
		self.vbox.pack_start(self.image)

		self.statusbar = gtk.Statusbar()
		self.vbox.pack_end(self.statusbar, False, True)

		self.window.show_all()

	def set_nodes(self, nodes):
		self.nodes = nodes
		self.draw()

	def main(self):
		gtk.gdk.threads_enter()
		gtk.main()
		gtk.gdk.threads_leave()
