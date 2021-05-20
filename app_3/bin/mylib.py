# -*- coding: utf-8 -*-

import os
import tkinter, tkinter.filedialog, tkinter.messagebox
import pandas as pd
import numpy as np
import datetime
from tqdm import tqdm
import json
from pathlib import Path


def handleDialog(f):
	path = ""

	root = tkinter.Tk()
	root.attributes("-topmost", True)
	root.withdraw()
	iDir = Path.cwd()
	fTyp = [("","*",)]

	if f == 0:	# file path
		path = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
	else:		# folder path
		path = tkinter.filedialog.askdirectory(initialdir = iDir)

	return path


def getpath(title="", msg=""):
	# root = tkinter.Tk()
	# root.withdraw()
	# fTyp = [("","*",)]
	# iDir = os.path.abspath(os.path.dirname(__file__))
	# tkinter.messagebox.showinfo(title, msg)
	# file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
	# print(file)

	# dev mode
	if os.name == "nt":
		file = "C:/Users/1give/private/task/app_3/bin/def/d_mainfile.csv"
	else:
		file = "/Users/jsakaguc/Documents/workspace/portfolio/private/task/app_3/bin/def/d_mainfile.csv";
	return file

def getConf(self):
	conf = {}
	rows = []
	path = "%s/bin/conf.d" % self.path
	with open(path, 'r', encoding="utf-8") as f:
		rows = f.read().split("\n")
	for i in range(0, len(rows)):
		if '#' in rows[i]:
			row = rows[i+1].split(':')
			if "current" in rows[i]:
				if len(row[1].strip()) == 0:
					conf["current"] = os.getcwd()
				else:
					conf["current"] = row[1].strip()
			elif 'setting file' in rows[i]:
				conf["settingfile"] = row[1].strip()
			elif 'post list' in rows[i]:
				conf["postList"] = row[1].strip()
			elif 'IPadress' in rows[i]:
				self.ip = row[1].strip()
			elif 'port' in rows[i]:
				self.port = row[1].strip()
			elif 'group' in rows[i]:
				conf["groupPath"] = row[1].strip()
			elif 'masterfile' in rows[i]:
				conf["masterfilePath"] = row[1].strip()
			elif "output" in rows[i] and ':' not in rows[i]:
				conf["output"] = row[1].strip()
			i += 1
	print("- get Configuration data\t...done.")
	return conf

def getSettingParams(self):
	path = "%s/%s" % (self.path, self.conf["settingfile"])
	if os.path.exists(path) is False:
		path = getpath("fail", "* select .json setting data params.")
	with open(path, encoding="utf-8") as f:
		dic = json.load(f)
	print("- get Data params\t...done.")
	return dic

def getRegionalMap(self, masterfile):
	self.regionalmap = {}
	print(masterfile.columns)
	df = masterfile[["病院名漢字", 'KENALL１', 'KENALL２', "自治体１", "自治体２", "自治体３"]]

	print(df.head())
	return None

def getMasterfile(self, masterpath):
	path = "%s/%s" % (self.path, masterpath)
	masterfile = pd.read_excel(path)
	getRegionalMap(self, masterfile)
	self.fileparams["masterfile"]["read_col"] = masterfile.columns.to_list()
	df = masterfile[ self.fileparams["masterfile"]["read_col"] ]
	# df = df[df["コロナあり"] != 0].set_index("ｺｰﾄﾞ")
	df = df.set_index("ｺｰﾄﾞ")
	df = df.rename( columns=self.fileparams["masterfile"]["df_rename_col"] )

	with open("%s/%s" % (self.path, self.conf["settingfile"]), "w", encoding="utf-8") as f:
		json.dump(self.fileparams, f, indent=2, ensure_ascii=False)
	return df

def getMainfile(self):
	f = []
	try:
		file = getpath("main file", "select the data file '.csv'.")
		df = pd.read_csv(file)
		df = df[
			self.fileparams["mainfile"]["read_col"]
		]
	except Exception as e:
		raise
	df = df.rename(
		columns=self.fileparams["mainfile"]["df_rename_col"]
	)

	dateset = df["受付日"].values.tolist()
	self.date = dateset[0]

	print("- get mainfile\t...done.")
	return df

def getGroup(path, file):
	df = pd.read_csv("%s/bin/def/%s" % (path, file), index_col=0)
	dic = df.to_dict(orient='index')

	for k, v in dic.items(): v["filename"] = None

	print("- get Group data\t...done.")
	return dic

def convdate(d):
	ptime = datetime.datetime.strptime(d, "%Y%m%d")
	return ptime.strftime("%Y/%m/%d")

def getDateList(self):
	li = []
	path = "%s/%s" % (self.path, self.conf["output"])
	files = os.listdir(path)
	files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]
	li = [[f, convdate(f)] for f in files_dir]
	print("- get date list\t...done.", '\n')
	return li

# --- //constructor------------------------------------------------------------

def savefile(self, path, df, prf):
	path = "%s/%s" % (path, self.date)
	if os.path.exists(path) is False: os.mkdir(path)

	if prf not in self.group.keys():
		self.group[prf] = {"email": None, "filename": None, "size": 0}

	savefile = "%s/%s_%s.csv" % (path, self.date, prf)
	df = df.drop(columns=self.fileparams["output"]["drop_params"])
	# df.to_csv(savefile)
	print("* create file: %s_%s.csv\t...done." % (self.date, prf))

	self.group[prf]["filename"] = "%s_%s.csv" % (self.date, prf)
	self.group[prf]["size"] = len(df)

	return None

def setDf(self):
	hp_codedf = self.mainfile["病院ｺｰﾄﾞ"]
	hp_codelist = list(set(hp_codedf.values.tolist()))
	data = {}

	savepath = "%s/%s" % (self.conf["current"], self.conf["output"])

	print("- Concat mainfile splited in prefecture with masterfile.\n")
	pbar = tqdm(total=len(self.mainfile))
	for code in hp_codelist:
		# mainfileから病院コード単位で抽出
		rows = self.mainfile[self.mainfile["病院ｺｰﾄﾞ"] == code]
		rows = rows.reset_index().rename(columns={"index": "id"})

		# masterから病院コードの行を抽出
		master = self.masterfile[self.masterfile.index == code]
		master = master.drop("病院名漢字", axis=1)
		prefecture = master["KENALL１"].values[0]

		# duplicate rows
		mst_data = master
		for i in range(len(rows)-1):
			master = master.append(mst_data)
		master["id"] = rows["id"].values

		conData = rows.merge(master)

		data[prefecture] = conData if prefecture not in data.keys() else pd.concat([data[prefecture], conData])

		pbar.update(len(rows))
	pbar.close()
	print("\n- save files by prefecture.")
	# save data
	for k, v in data.items():
		savefile(self, savepath, v, k)
	print("\n- set dataset\t ...done.\n")
	return None

def overWriteConf(self, newData):
	print(newData)
	return None
