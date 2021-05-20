# -*- coding: utf-8 -*-

import pprint
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from os.path import basename

from bin.mylib import *
from bin.MailLib import *

class HandleData:
	def __init__(self):
		return None

	def getInit(self):
		self.date = None
		self.desc = {}
		self.path = os.getcwd()
		self.conf = getConf(self)
		self.fileparams = getSettingParams(self)
		self.mainfile = getMainfile(self)
		self.pool = {}
		self.masterfile = getMasterfile(self, self.conf["masterfilePath"])
		self.group = getGroup(self.path, self.conf["groupPath"])
		self.datelist = getDateList(self)

	def main(self):
		self.dataset = setDf(self)
		return None

	# def output(self):
	# 	outputfile = "%s/%s" % self.conf.output
	# 	return None

	def get_datefolderlist(self, date):
		li = []
		path = "%s/%s/%s" % (self.path, self.conf["output"], date)
		files = os.listdir(path)
		files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]
		print(files_file)
		return files_file

	def postfile(self):
		self.info = getInfo(self)
		self.fld = "%s/result/%s" % (self.conf["current"], self.date)
		# to_email = "knowprj36l1@gmail.com"
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.set_debuglevel(True)
		server.ehlo()
		server.login(self.info["from_email"], self.info["password"])

		for k, v in self.group.items():
			try:
				pass
				msg = postMail(self, k, v)
				server.sendmail(self.info["from_email"], v["email"], msg)
				print("* post email to %s\n" % k)
			except Exception as e:
				print("* fail to send email to %s\n" % k)
				continue
		server.close()
		return None
