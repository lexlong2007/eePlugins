 # -*- coding: utf-8 -*-
from Poll import Poll
from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import fileExists
from os import popen

class BlackHarmonyHddTempInfo(Poll, Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.type = type
		self.poll_interval = 2000
		self.poll_enabled = True
	
	@cached
	
	def getText(self):
		info = 'N/A'
		if fileExists("/usr/sbin/hddtemp") and fileExists("/dev/sda"):
			info = "%s%sC" % (popen("hddtemp -n -q /dev/sda").read().strip('\n'), unichr(176).encode('utf-8'))
		return info
	
	text = property(getText)
	
	def changed(self, what):
		if what[0] == self.CHANGED_POLL:
			self.downstream_elements.changed(what)
