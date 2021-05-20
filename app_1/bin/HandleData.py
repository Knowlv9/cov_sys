# -*- coding: utf-8 -*-
import os
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import time
import pandas as pd
import csv

from src.backend.bin.mylib import *

class HandleData:
	def __init__(self, f):
		self.file = f
		self.max_id = 90000
		self.lastSEQ = 0
		self.hp_names = pd.read_json("./src/data/Dev/hp_names_dev.json")		# Dev Mode
		self.basefile = getfile("./src/data/Dev/d_sample.csv")					# Dev Mode
		self.data = ""

	def initData(self):
		data = []
		path = './src/data/Order/%s' % self.file
		dic = getfile(path)

		for d in dic:
			if int(d['idx']) > self.max_id:
				self.max_id = int(d["idx"])
			if int(d['SEQ']) > self.lastSEQ:
				self.lastSEQ = int(d["SEQ"])

			data.append({
				'id': int(d['idx']),
				'SEQ': int(d["SEQ"]),
				'name': d['name'],
				'hp_name': d['hp_name'],
				'sex': int(d['sex']),
				'birthday': d['birthday'],
				'specimen': int(d['specimen']),
				'expire': int(d['expire']),
				'office': d['office'],
				'code': self.hp_names[d["hp_name"]].code
			})
		return data

	def setDevData(self):
		if len(self.data) > 20: return None

		data = []

		for d in self.basefile:
			data.append({
				'idx': int(d['id']),
				'SEQ': 0,
				'name': d['name'],
				'hp_name': d['hp_name'],
				'sex': int(d['sex']),
				'birthday': str(d['birthday']),
				'specimen': int(d['specimen']),
				'expire': int(d['expire']),
				'office': d['office'],
				'code': self.hp_names[d["hp_name"]].code
			})
		return None

	def addDataByCode(self, newData):
		f = True
		for d in newData:
			if d["regi"] is True:
				self.lastSEQ += 1
				d["SEQ"] = self.lastSEQ
			else:
				d["SEQ"] = 0
			d.pop("regi")
			if d["id"] is None:
				self.max_id += 1
				d["id"] = self.max_id
		idx = [d["id"] for d in newData]
		print(newData)
		newdf = pd.DataFrame(newData).set_index('id')
		df = pd.DataFrame(self.data).set_index("id")
		condf = pd.concat([df, newdf])
		print(condf)
		return f
