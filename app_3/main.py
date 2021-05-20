# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, make_response, jsonify
from flask_cors import CORS
import os

from bin.HandleData import HandleData


app = Flask(__name__, static_folder="./src/static", template_folder="./src/temp")
CORS(app)
app.config['JSON_AS_ASCII'] = False
app.config["JSON_SORT_KEYS"] = False

# @app.after_request
# def after_request(response):
#   response.headers.add('Access-Control-Allow-Origin', '*')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#   return response

@app.route("/", methods=['GET'])
def index():
	return render_template("loding.html")

@app.route("/home", methods=['GET'])
def home():
	data = {}
	path = "./%s/%s" % (hd.conf["output"], hd.date)

	return render_template("home.html", path=path, group=hd.group, p=0,
		datelist=hd.datelist)

@app.route("/register", methods=['GET'])
def register():
	return render_template("register.html", p=1)

@app.route("/post", methods=['GET'])
def post():
	print(hd.conf["postList"])
	return render_template("post.html", group=hd.group, p=2, datelist=hd.datelist)

@app.route("/show_list", methods=['POST'])
def show_list():
	datelist = {}
	if request.method == "POST":
		date = request.form["date"]
		datelist["list"] = hd.get_datefolderlist(date)
		datelist["result"] = True
	else:
		datelist["result"] = False
	return make_response(jsonify(datelist))


@app.route("/setting", methods=['GET'])
def setting():
	# print(hd.fileparams)
	return render_template("setting.html", conf=hd.conf, params=hd.fileparams, p=3)

@app.route("/getFileparams", methods=['GET'])
def getFileparams():
	return make_response(jsonify(hd.fileparams))

@app.route("/getDirectory", methods=['GET'])
def getDirectory():
	result = hd.getDirpath()
	return make_response(result)

@app.route("/getFilePath", methods=['GET'])
def getFilePath():
	result = hd.getfilepath()
	return make_response(jsonify({"file": result}))

@app.route("/settingMasterfile", methods=['POST'])
def settingMasterfile():
	data = {}

	if request.method == "POST":
		input_conf = {
			"masterfilePath": request.form["masterfilepath"],
			"output": request.form["outputfilepath"],
		}
		out_cols = request.form["outputColList"].split(',')
		data["result"] = hd.editConf(confData=input_conf, out_cols=out_cols)
	return make_response(jsonify(data))

@app.route("/postfile", methods=['GET'])
def postfile():
	data = {
		"hello": "world"
	}
	hd.postfile()
	return make_response(jsonify(data))


if __name__ == "__main__":
	hd = HandleData()
	print("""
	-+--------------------------------------------------------------------- + -
	 	Start SARS-Cov-2 test Create Report
	-+--------------------------------------------------------------------- + -
	""")
	hd.getInit()
	hd.main()
	if os.name == "nt":
		app.run(host=hd.ip, port=hd.port, debug=True)
	else:
		app.run(host="localhost", port="5000", debug=True)
