# -*- coding: utf-8 -*-
import csv, json
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import time
import numpy as np
import pandas as pd
import pprint
from src.backend.bin.Reslib import newfilename, createfile
from src.backend.bin.mylib import encodeJa

def getfile(path):
	file =  open(path, 'r', encoding="utf-8", errors="")
	return csv.DictReader(file, delimiter=",", doublequote=True)

def debug_rec_data(f):
	f = getfile('./src/data/Order/%s' % f)
	hp_file = pd.read_json("./src/data/Dev/hp_names_dev.json")
	data = []
	for d in f:
		data.append({
			'id': int(d['idx']),
			'SEQ': int(d["SEQ"]),
			'name': d['name'],
			'hp_name': d['hp_name'],
			'sex': int(d['sex']),
			'birthday': getAge(d['birthday']),
			'specimen': int(d['specimen']),
			'expire': int(d['expire']),
			'office': d['office'],
			'code': hp_file[d["hp_name"]].code
		})
	return data

# ------------------------------------------------------------------

def getAge(d):
	a = dt.strptime(d, '%Y/%m/%d')
	today = dt.today()
	dlt = relativedelta(today, a)
	return dlt.years
	return d

def get_num_hp(arr, hp):
	n = 0
	for r in arr:
		if r['hp_name'] == hp:
			n += 1
		else:
			break
	return n


def uploadData(bdf, path):
	wdf = pd.read_csv(path, index_col='idx')
	diff = [bdf[~bdf.index.isin(wdf.index)]]
	idx_diff = [x for x in bdf.index if x in wdf.index]
	df = bdf.drop(index=idx_diff)
	wdf = wdf.append(df)
	wdf.to_csv(path, index=True)
	return None

def conv_csvTodt(data):
	arr = []
	hp_file = pd.read_json("./src/data/Dev/hp_names_dev.json")
	for d in data:
		arr.append({
			'idx': int(d['id']),
			'SEQ': 0,
			'name': d['name'],
			'hp': d['hp_name'],
			'sex': int(d['sex']),
			'birthday': str(d['birthday']),
			'sample': int(d['specimen']),
			'expire': int(d['expire']),
			'office': d['office'],
			'code': hp_file[d["hp_name"]].code
		})
	return pd.DataFrame(arr).set_index('idx').sample()

def debuger():
	basefilename = getfile("./src/data/Dev/d_sample.csv")
	hp_file = pd.read_json("./src/data/Dev/hp_names_dev.json")
	data = []

	for d in basefilename:
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
			'code': hp_file[d["hp_name"]].code
		})
		break

	idx = 0
	arr = list(range(0, 7))
	df = pd.DataFrame(data)
	while (idx < len(data)-1):
		# time.sleep(5)
		hp = data[idx]['hp_name']
		n = np.random.choice(arr, size=1, p=[1/len(arr)]*len(arr))[0]
		updateList = []
		for j in range(0, n):
			num = get_num_hp(data[idx:], hp)
			updateList.extend(data[idx:idx+num])
			idx = idx + num if j == 0 else idx + num
			try:
				hp = data[idx]['hp_name']
			except Exception as e:
				break
		# print('updateList length:', len(updateList))
		if len(updateList) > 0:
			uploadData(pd.DataFrame(updateList).set_index('idx'), "./src/data/Order/%s" % newfilename())
		# break
		if idx > 100: break
	return None

def addItems():
	li = list(range(3, 11))
	p = [1/len(li)] * len(li)
	n = np.random.choice(li, size=1, p=p)
	return n[0]

def getNewData(last, source):
	data = []
	diff_id = list(set(source['id']) - set(last.index))
	hp_file = pd.read_json("./src/data/Dev/hp_names_dev.json")
	N = addItems()

	for id in diff_id:
		if N <= 0: break

		d = source[source.id == id]
		data.append({
			'idx': int(d['id']),
			'SEQ': 0,
			'name':  d['name'].iloc[-1],
			'hp_name': d['hp_name'].iloc[-1],
			'sex': int(d['sex']),
			'birthday': d['birthday'].iloc[-1],
			'specimen': int(d['specimen']),
			'expire': int(d['expire']),
			'offic	e': d['office'].iloc[-1],
			'code': hp_file[d['hp_name']].T.code.iloc[-1]
		})

		N -= 1
	data = pd.DataFrame(data)
	data.set_index('idx', inplace=True)
	return data

def ReceptIds(ids, path):
	data = pd.read_csv(path, index_col=0)
	seq = data['SEQ'].max() + 1
	# print(data.head())
	for id in ids:
		# print(data.at[id, 'SEQ'])
		if data.at[id, 'SEQ'] != 0:
			print("%s: cannot set SEQ" % (id))
		else:
			data.at[id, 'SEQ'] = seq
			seq += 1
	# print(data.head())
	data.to_csv(path, index=True, encoding="utf-8")
	return None

# --*-- develop -------------------------------------------------------------*
import pprint
import os, json
from scipy import stats
import barcode
from barcode.writer import ImageWriter
import qrcode
import random
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Padding

class AESCipher(object):
	def __init__(self, key):
		self.key = (hashlib.md5(key.encode('utf-8')).hexdigest()).encode('utf-8')

	def encrypt(self, raw):
		iv = Random.get_random_bytes(AES.block_size)
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		data = Padding.pad(raw.encode('utf-8'), AES.block_size, 'pkcs7')
		return base64.b64encode(iv + cipher.encrypt(data))

	def decrypt(self, enc):
		enc = base64.b64decode(enc)
		iv = enc[:AES.block_size]
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		data = Padding.unpad(cipher.decrypt(enc[AES.block_size:]), AES.block_size, 'pkcs7')
		return data.decode('utf-8')

def get_blankdata(n, d):
	if n <= 0:
		d["info"]["name"] = None
	if n <= 1:
		d["info"]["sex"] = None
		d["info"]["age"] = None
	return d

import string

def get_patient(path):
	d_sample = getfile(path)
	df = conv_csvTodt(d_sample)
	i = df.index[0]
	sr = df.loc[i]
	data = {
		'id': int(i),
		'info': {
			'name': encodeJa(sr["name"]),
			'sex': int(df['sex']),
			'age': sr["birthday"]
		},
		'expire': int(sr["expire"]),
		'hp_code': int(sr["code"]),
		'office': str(sr["office"])
	}

	plainText = ""
	n = np.random.choice(list(range(0,3)), size=1, p=[1/3]*3)[0]
	data = get_blankdata(n, data)

	for k, v in data.items():
		if k == "info":
			plainText += "info:%s@%s@%s," % (v["name"], v["sex"], v["age"])
		else:
			plainText += "%s:%s," % (k, v)
	key = ''.join([str(i) for i in range(23, 120, 7)]) + "9"
	cipher = AESCipher(key)

	encrypted = cipher.encrypt(str(plainText.rstrip(',')))
	# decrypted = cipher.decrypt(encrypted)


	code = "%s%s%s" % (
		str(data["hp_code"]).zfill(6),
		str( int(random.random() * 1000) ).zfill(5),
		str(data["id"]).zfill(6))
	ean = barcode.get_barcode_class('code128')
	bar = ean(code, writer=ImageWriter() )

	os.mkdir("./public/bin/codec/%s" % code)
	path = "./public/bin/codec/%s" % code
	bar.save("%s/barcode" % path)

	qr = qrcode.make(encrypted)
	qr.save("./public/bin/codec/%s/qrcode.png" % code)
	data["path"] = "./bin/codec/%s" % code

	return data
# //*-- develop -------------------------------------------------------------*

def nameDecrypt(dcr):
	if dcr == "None": return None

	f = open("./src/backend/bin/decryptJa.json", 'r', encoding='utf-8')
	key = json.load(f)
	i = 0
	name = ""

	while i < len(dcr):
		e = dcr[i: i+2]
		name += key[e]
		i += 2
	return name

def moldingData(strData):
	dic = {}
	strData = strData.split(',')
	# print(strData)
	for items in strData:
		item = items.split(':')
		if "name" == item[0]:
			dic["name"] = nameDecrypt(item[1])
		else:
			dic[item[0]] = int(item[1]) if item[1].isdigit() else item[1]
	# 	print(item)
	# print(dic)
	return dic

def myDecode(c):
	data = {"encrypt": c, "decrypt": None}
	if len(c) > 32:
		key = ''.join([str(i) for i in range(23, 120, 7)]) + "9"
		cipher = AESCipher(key)
		decrypted = cipher.decrypt(c)
		print(decrypted)
		data["decrypt"] = moldingData(decrypted)
	else:
		data["decrypt"] = int(c.strip())
	return data["decrypt"];























#
