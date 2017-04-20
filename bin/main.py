#!/usr/bin/python

import wiringpi
import urlparse
import time
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from objects import *

global queue

class myHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		reply = ''
		self.send_response(200)
   		self.send_header("Content-type", "text/html")
		self.end_headers()
		parsed = urlparse.urlparse(self.path)	
		action = urlparse.parse_qs(parsed.query)['action'][0]
		print "[http] Requested action: " + action
		if action == "getconfig":
			id = int(urlparse.parse_qs(parsed.query)['id'][0])
			reply = main.blinders[id].config()
		elif action == "autoaction":
			id = int(urlparse.parse_qs(parsed.query)['id'][0])
                        main.blinders[id].autoaction()
		elif action == "getstate":
			id = int(urlparse.parse_qs(parsed.query)['id'][0])
                        reply = main.blinders[id].getstate()
		elif action == "queuelen":
                        reply = 'Processing objects: ' + str(len(queue)) + '\n'
		self.wfile.write(reply)
		return

class Main():

	config = []
	blinders = []
	def __init__(self):
		print "Initialization started"
		raw_json = open("../config/config.json").read()
		self.config = json.loads(raw_json)
		print "Config file version: " + self.config['version']
		print "Preparing blinders..."
		for i in self.config['group']:
			print "  + Group: " + i['name']
			for j in i['blinders']:
				print "    " + j['name'] + "\t" + j['description']
				self.blinders.insert(j['id'], Blinder(pinup=j['pinup'], pindown=j['pindown'], time=j['wtime'], name=j['name']))
		print "Initialized " + str(len(self.blinders)) + " objects"
		print "Initialization finished"

	def Config(self):
		print self.config

if __name__ == "__main__":
    try:
	main = Main()
	server = HTTPServer(('', 80), myHandler)
	server.serve_forever()
    except KeyboardInterrupt:
	print('Ctrl+C received, shutting down... Bye.')

