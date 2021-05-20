# -*- coding: utf-8 -*-
import os
from src.backend.bin.Reslib import newfilename, createfile

class Mother:
	def __init__(self):
		self.data = None
		self.workfile = newfilename()

	def initialSetting(self):
		print("initialSetting")
		if os.path.exists("./src/data/Order/%s" % self.workfile ) is False:
			createfile()
		return None
