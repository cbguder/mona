#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class ProgressDialog(gtk.Dialog):
	def __init__(self, title=None, parent=None):
		gtk.Dialog.__init__(self, title, parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)

		self.vbox.remove(self.action_area)

		self.set_resizable(False)
		self.set_has_separator(False)
		self.set_border_width(10)
		self.vbox.set_spacing(10)

		self.label = gtk.Label(title)
		self.vbox.pack_start(self.label, True, True)

		self.progress_bar = gtk.ProgressBar()
		self.progress_bar.set_size_request(256, 32)
		self.progress_bar.set_text('0%')
		self.vbox.pack_end(self.progress_bar, True, True)

		self.show_all()

	def set_fraction(self, fraction):
		self.progress_bar.set_fraction(fraction)
		self.progress_bar.set_text('%d%%' % (100*fraction))
