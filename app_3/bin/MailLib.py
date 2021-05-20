# -*- coding: utf-8 -*-

import os, json
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from os.path import basename

def getInfo(self):
	path = "%s/bin/def/mailconf.json" % self.path
	with open(path, encoding="utf-8") as f:
		info = json.load(f)
	return info

def createText(f_name, r_name, prf):
	path = "./bin/def/mailTextTemp.txt"
	with open(path, encoding="utf-8") as f:
		text = f.read()
	text = text % (prf, r_name, r_name, f_name)
	return text

def postMail(self, prf, v):
	print(prf, v)
	message = createText(
	"from name",
	"Recipient name",
	prf
	)

	msg = MIMEMultipart()
	msg["Subject"] = "test1"
	msg["From"] = self.info["from_email"]
	msg["To"] = v["email"]
	msg["Date"] = formatdate()
	msg.attach(MIMEText(message))
#
	filepath = "%s/%s" % (self.fld, v["filename"])
	# print(filepath)
	if os.path.exists(filepath) and type(v["email"]) is not "float":
		with open(filepath, 'rb') as f:
			ma = MIMEApplication(
				f.read(),
				Name=basename(filepath)
			)
		ma["Content-Disposition"] = 'attachment; filename="%s"' % basename(filepath)
		msg.attach(ma)

	return msg.as_string()
