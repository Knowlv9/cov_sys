# -*- coding: utf-8 -*-
import os
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import time
import pandas as pd
import csv

ja = {
	'ァ': '71',  'ア': '9c',  'ィ': '97',  'イ': '78',  'ゥ': 'd4',  'ウ': 'ae',
	'ェ': '88',  'エ': 'a7',  'ォ': 'a5',  'オ': 'c9',  'カ': '85',  'ガ': '98',
	'キ': 'dd',  'ギ': 'de',  'ク': 'd2',  'グ': '8e',  'ケ': 'cc',  'ゲ': '70',
	'コ': '7f',  'ゴ': 'c8',  'サ': '64',  'ザ': '89',  'シ': '7e',  'ジ': '86',
	'ス': 'd3',  'ズ': '6e',  'セ': '72',  'ゼ': 'a1',  'ソ': 'ad',  'ゾ': 'cb',
	'タ': '7b',  'ダ': 'a0',  'チ': '7c',  'ヂ': '68',  'ッ': '8d',  'ツ': '83',
	'ヅ': '9d',  'テ': 'a2',  'デ': '6f',  'ト': '79',  'ド': 'aa',  'ナ': 'd6',
	'ニ': '82',  'ヌ': '67',  'ネ': '91',  'ノ': '87',  'ハ': '8c',  'バ': '69',
	'パ': '66',  'ヒ': '73',  'ビ': '84',  'ピ': 'a3',  'フ': 'ca',  'ブ': 'af',
	'プ': '9b',  'ヘ': '6b',  'ベ': '7d',  'ペ': 'd8',  'ホ': 'd9',  'ボ': 'a6',
	'ポ': '65',  'マ': 'cf',  'ミ': '99',  'ム': '96',  'メ': 'd7',  'モ': '7a',
	'ャ': 'b1',  'ヤ': '6a',  'ュ': '74',  'ユ': 'a4',  'ョ': 'df',  'ヨ': '90',
	'ラ': 'ab',  'リ': 'ce',  'ル': 'ac',  'レ': '9a',  'ロ': 'dc',  'ヮ': 'd5',
	'ワ': '8f',  'ヰ': 'cd',  'ヱ': '75',  'ヲ': 'b0',  'ン': '92',  'ヴ': '93',
	' ': 'ss'
}

c_ja = {v: k for k, v in ja.items()}

def encodeJa(strlist):
	code = []
	for s in strlist:
		try:
			code.append(ja[s])
		except Exception as e:
			break
	# print(code)
	return ''.join(code)

def decodeJa(code):
	ja = []
	i = 0
	while i > len(code):
		s = code[i:i+2]
		i += 2

def getAge(d):
	a = dt.strptime(d, '%Y/%m/%d')
	today = dt.today()
	dlt = relativedelta(today, a)
	return dlt.years
	return d

def getfile(path):
	file =  open(path, 'r', encoding="utf-8", errors="")
	return csv.DictReader(file, delimiter=",", doublequote=True)
