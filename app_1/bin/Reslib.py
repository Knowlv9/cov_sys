# -*- coding: utf-8 -*-
import datetime, time
import pandas as pd
import os, json,csv
import shutil

filedir = "./src/data/Order"
now = datetime.datetime.now()

def newfilename():
	today = datetime.datetime.now()
	day = today if today.hour > 21 else today - datetime.timedelta(days=1)
	return day.strftime("Cov_%Y%m%d.csv")

# 5分ごとにsample_1.csvから10件ずつnew_fileを更新する
def dev_update_data():
	for i in range(0, 1000):
		t = time.sleep(300)
		return i

def dev_rec_data(t):
	filedir = './../../data'
	filename = "%s/sample_1.csv" % (filedir)
	csv = pd.read_csv(filename, index_col=0)[0:t]
	# base_csv.to_csv("%s/%s" % (filedir, newfilename()), encoding="utf-8")
	return csv

def rec_data():
	filename = "%s/%s" % (filedir, newfilename())
	csv_file = open(filename, 'r', encoding="utf-8", errors="")
	data_csv = csv.DictReader(csv_file, delimiter=",", doublequote=True)
	# header = next(data_csv)
	# print(header)
	data = []
	for r in data_csv:
		# print(r)
		data.append({
			"name": r["氏名"],
			"katakana": r["氏名（カタカナ）"],
			"sex": int(r["性別"]),
			"birthday": r["生年月日"],
			"hp_name": r["病院名"],
			"sample": r["材料"],
			"expire": r["報告期限"]
		})
	# csv = pd.read_csv(filename, index_col=0)
	return data

def createfile():
	# create Order file
	path = './src/data/Order'
	in_f = "%s/Temp_Cov.csv.bak" % path
	out_f = "%s/%s" % (path, newfilename())
	shutil.copy(in_f, out_f)

	# create Info file
	path = "./src/data/Info"
	in_f = '%s/Temp_Info.csv.bak' % path
	out_f = "%s/%s" % (path, newfilename().replace("Cov", "Info"))
	shutil.copy(in_f, out_f)
	return None

# if __name__ == "__main__":
# 	data = dev_rec_data()
