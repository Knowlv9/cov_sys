# -*- coding: utf-8 -*-
import csv
import os
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import time
import numpy as np
import pandas as pd
import pprint
from src.backend.bin.Reslib import newfilename

def debug_rec_data(f):
	f = getfile('./src/data/%s' % f)
	# for r in f:
	# 	print(r)
	data = {
		"data" : "hello world",
		'greetinh': "こんにちは"
	}
	return data

# ------------------------------------------------------------------

def getAge(d):
	a = dt.strptime(d, '%Y/%m/%d')
	today = dt.today()
	dlt = relativedelta(today, a)
	return dlt.years

def get_num_hp(arr, hp):
	n = 0
	for r in arr:
		if r['病院名'] == hp:
			n += 1
		else:
			break
	return n

def getfile(path):
	file =  open(path, 'r', encoding="utf-8", errors="")
	return csv.DictReader(file, delimiter=",", doublequote=True)

def uploadData(bdf, path):
	wdf = pd.read_csv(path, index_col='id')
	diff = [bdf[~bdf.index.isin(wdf.index)]]
	idx_diff = [x for x in bdf.index if x in wdf.index]
	df = bdf.drop(index=idx_diff)
	wdf = wdf.append(df)
	wdf.to_csv(path, index=True)
	return None

# 3～5分ごとに作業用csvファイルを更新する
# 更新はd_sample.csvからnつの病院を選択する
def debuger():
	basefilename = getfile("./src/data/d_sample.csv")
	data = []
	for d in basefilename:
		data.append({
			'id': int(d['id']),
			'氏名（カタカナ）': d['氏名（カタカナ）'],
			'病院名': d['病院名'],
			'性別': int(d['性別']),
			'生年月日': getAge(d['生年月日']),
			'材料': int(d['材料']),
			'報告期限': int(d['報告期限']),
			'営業所': d['営業所']
		})
	# pprint.pprint(data)
	idx = 0
	arr = list(range(0, 5))
	df = pd.DataFrame(data)
	while (idx < len(data)-1):
		time.sleep(5)
		hp = data[idx]['病院名']
		n = np.random.choice(arr, size=1, p=[1/len(arr)]*len(arr))[0]
		updateList = []
		for j in range(0, n):
			num = get_num_hp(data[idx:], hp)
			updateList.extend(data[idx:idx+num])
			idx = idx + num if j == 0 else idx + num
			hp = data[idx]['病院名']
		print('updateList length:', len(updateList))
		if len(updateList) > 0:
			uploadData(pd.DataFrame(updateList).set_index('id'), "./src/data/%s" % newfilename())
		# break
		if idx > 50: break
	return None
