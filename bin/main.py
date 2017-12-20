#!/usr/bin/python

import traceback
import wiringpi
import urlparse
import time
import json
import threading
import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from objects import *

global queue

def log_action(module, message):
	mytime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	text = mytime + "  [" + module + "] " + message
	print text

class myHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		reply = ''
		self.send_response(200)
   		self.send_header("Content-type", "text/html")
		self.end_headers()
		parsed = urlparse.urlparse(self.path)	
		try:
			action = urlparse.parse_qs(parsed.query)['action'][0]
			log_action("http", "Requested action: " + action)
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
		except:
			log_action("http", "Unknown action, sending index.html")
			os.chdir('../www')
			reply = open(self.path[1:]).read()
			self.wfile.write(reply)
			traceback.print_exc()
		return

	def log_message(self, format, *args):
		return

class Main():

	config = []
	blinders = []
	pin_base = 65
	i2c_addr = 0x27
	def __init__(self):
		print "Initialization started"
		raw_json = open("../config/config.json").read()
		self.config = json.loads(raw_json)
		print "Config file version: " + self.config['version']
		try:
			wiringpi.wiringPiSetup()
			wiringpi.mcp23017Setup(65, 0x27)
			wiringpi.mcp23017Setup(81, 0x26)
		except:
			print "Initialization MCP23017 I2C failed."
		else:
			print "Initialized MCP23017 I2C"
		print "Preparing blinders..."
		for i in self.config['group']:
			print "  + Group: " + i['name']
			for j in i['blinders']:
				print "    " + j['name'] + "\t" + j['description']
				pup = j['pinup'] + 65
				pdown = j['pindown'] + 65
				self.blinders.insert(j['id'], Blinder(pinup=pup , pindown=pdown, time=j['wtime'], name=j['name']))
		print "Initialized " + str(len(self.blinders)) + " objects"
		print "Initialization finished. Ready to rock.\n"

	def Config(self):
		pass


class QueueThread(threading.Thread):
	def run(self):
		log_action('queuerunner', 'Queue thread started')
		while True:
			time.sleep(0.05)                                  
			if len(queue) > 0:                                
				for i in queue:                           
					i.timeout()                       
	
		



if __name__ == "__main__":
    try:
	main = Main()
	queuerunner = QueueThread()
	queuerunner.daemon = True
	queuerunner.start()
	server = HTTPServer(('', 80), myHandler)
	server.serve_forever()
    except KeyboardInterrupt:
	print('Ctrl+C received, shutting down... Bye.')

