from flask import Flask
from flask import render_template
from flask import request
from redis import Redis
import sys
import optparse
import time
import json

import os
import socket

app = Flask(__name__)
redis = Redis(host='redis', port=6379)
#redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

visits = 5

start = int(round(time.time()))

@app.route("/")
def index():
	return render_template('index.html')


@app.route("/add")
def addStudent():
	a = str(request.args.get('a'))
	b = str(request.args.get('b'))
	redis.set(a,b)
	return "Added"


@app.route("/search")
def searchStudent():
	s = str(request.args.get('a'))
	searchGrade = redis.get(s)
	if searchGrade == None :
		return "No Results"
	else : 
		return searchGrade

@app.route("/del")
def delStudent():
	s = str(request.args.get('a'))
	searchGrade = redis.get(s)
	if searchGrade == None :
		return "No Results"
	else : 
		redis.delete(s)
		return "Deleted"

@app.route("/listAll")
def listStudents():
	rdict = {}
	rj = '{"data":['
	for key in redis.scan_iter("*"):
		rdict[key] = redis.get(key)
		if rj != '{"data":[' :
			rj = rj + ','
		rj = rj + '{"name":"' + key + '","grade":"' + redis.get(key) + '"}'
	rj = rj + ']}'
	jsonRes = json.dumps(rdict)

	return rj


# @app.route("/tes")
# def tes():
# 	return "hi"


if __name__ == '__main__':
    parser = optparse.OptionParser(usage="python simpleapp.py -p ")
    parser.add_option('-p', '--port', action='store', dest='port', help='The port to listen on.')
    (args, _) = parser.parse_args()
    if args.port == None:
        print "Missing required argument: -p/--port"
        sys.exit(1)
    app.run(host='0.0.0.0', port=int(args.port), debug=False)
