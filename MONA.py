#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

gtk.gdk.threads_init()

NODE_SIZE = 4

import sys
import time
from threading import Thread
from ProgressDialog import ProgressDialog
from TraceParser import TraceParser

class MONA:
	def window_delete(self, widget, event, data=None):
		return False

	def window_destroy(self, widget, data=None):
		gtk.main_quit()

	def draw(self):
		self.statusbar.push(0, '%.3f' % self.t)
		self.statusbar.queue_draw()

		rect = self.image.get_allocation()
		style = self.image.get_style()

		self.pos      = [n.position_at(self.t) for n in self.nodes]
		self.activity = [n.active_at(self.t) for n in self.nodes]

		pixmap = gtk.gdk.Pixmap(None, rect.width, rect.height, 24)
		pixmap.draw_rectangle(style.bg_gc[gtk.STATE_NORMAL], True, 0, 0, rect.width, rect.height)

		red = self.image.get_parent_window().new_gc()
		red.foreground = self.image.get_colormap().alloc_color("#FF0000")

		for i, p in enumerate(self.pos):
			if self.activity[i]:
				gc = red
			else:
				gc = style.fg_gc[gtk.STATE_ACTIVE]

			pixmap.draw_arc(gc, True,
			                int(rect.width  * (p.x / 1000.0) - NODE_SIZE/2),
			                int(rect.height * (p.y / 1000.0) - NODE_SIZE/2),
			                NODE_SIZE, NODE_SIZE,
			                0, 64 * 360)

		self.image.set_from_pixmap(pixmap, None)

	def do_step(self, forward=True):
		if forward:
			self.t += self.adjustment.value
		else:
			self.t -= self.adjustment.value
		self.draw()

	def previous_clicked(self, widget, data=None):
		self.do_step(False)

	def next_clicked(self, widget, data=None):
		self.do_step()

	def rewind_clicked(self, widget, data=None):
		self.fstop = True
		self.t = 0.0
		self.draw()

	def play(self):
		while self.t < 60 and not self.fstop:
			gtk.gdk.threads_enter()
			self.do_step()
			gtk.gdk.threads_leave()
			time.sleep(0.005)
		self.start.set_sensitive(True)
		self.previous.set_sensitive(True)
		self.next.set_sensitive(True)
		self.stop.set_sensitive(False)

	def start_clicked(self, widget, data=None):
		self.fstop = False
		self.previous.set_sensitive(False)
		self.next.set_sensitive(False)
		self.stop.set_sensitive(True)
		widget.set_sensitive(False)
		th = Thread(target=self.play)
		th.start()

	def stop_clicked(self, widget, data=None):
		self.fstop = True

	def parse_file(self):
		try:
			f = open(self.file)
		except IOError, e:
			gtk.gdk.threads_enter()
			d = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "Cannot open %s: %s" % (self.file, e.args[1]))
			d.run()
			d.destroy()
			gtk.gdk.threads_leave()
			return

		gtk.gdk.threads_enter()
		dialog = ProgressDialog('Parsing trace file...', self.window)
		gtk.gdk.threads_leave()

		parser = TraceParser()
		t = Thread(target=parser.parse, args=(f,))
		t.start()

		while t.isAlive():
			gtk.gdk.threads_enter()
			dialog.set_fraction(parser.progress)
			gtk.gdk.threads_leave()
			time.sleep(0.01)

		dialog.destroy()
		f.close()
		self.set_nodes(parser.get_nodes())

	def __init__(self, file):
		self.nodes = None
		self.t     = 0.0
		self.pos   = None
		self.fstop = False
		self.file  = file

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
		self.rewind.set_sensitive(False)
		self.hbox.add(self.rewind)

		self.previous = gtk.Button(None, gtk.STOCK_MEDIA_PREVIOUS)
		self.previous.connect('clicked', self.previous_clicked)
		self.previous.set_sensitive(False)
		self.hbox.add(self.previous)

		self.start = gtk.Button(None, gtk.STOCK_MEDIA_PLAY)
		self.start.connect('clicked', self.start_clicked)
		self.start.set_sensitive(False)
		self.hbox.add(self.start)

		self.next = gtk.Button(None, gtk.STOCK_MEDIA_NEXT)
		self.next.connect('clicked', self.next_clicked)
		self.next.set_sensitive(False)
		self.hbox.add(self.next)

		self.stop = gtk.Button(None, gtk.STOCK_MEDIA_STOP)
		self.stop.connect('clicked', self.stop_clicked)
		self.stop.set_sensitive(False)
		self.hbox.add(self.stop)

		self.adjustment = gtk.Adjustment(0.1, 0.001, 1.0, 0.001, 0.1)
		self.spinbutton = gtk.SpinButton(self.adjustment, 0.01, 3)
		self.hbox.add(self.spinbutton)

		self.image = gtk.Image()
		self.image.set_size_request(512, 512)
		self.vbox.pack_start(self.image)

		self.statusbar = gtk.Statusbar()
		self.vbox.pack_end(self.statusbar, False, True)

		self.window.show_all()

		t = Thread(target=self.parse_file)
		t.start()

	def set_nodes(self, nodes):
		self.nodes = nodes
		self.draw()
		self.start.set_sensitive(True)
		self.previous.set_sensitive(True)
		self.next.set_sensitive(True)
		self.rewind.set_sensitive(True)

	def main(self):
		gtk.gdk.threads_enter()
		gtk.main()
		gtk.gdk.threads_leave()
