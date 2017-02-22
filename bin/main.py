#!/usr/bin/python

import wiringpi
import urlparse
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from objects import *

global queue

wiringpi.wiringPiSetup()

rolety = {'roleta1':Blinder(0,2,3), \
	'roleta2':Blinder(6,3,6), \
	'roleta2':Blinder(65,66,5)}

button = Button(7, rolety['roleta1'])
button1 = Button(10, rolety['roleta2'])

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
	path = self.path
	par = urlparse.parse_qs(urlparse.urlparse(path).query)
	if par['blinder'][0] in rolety:
		print "Request dla: ",par['blinder'], " Kierunek: ", par['dir']
		rolety[par['blinder'][0]].button()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        return


if __name__ == "__main__":
    try:
	server = HTTPServer(('192.168.1.201', 8000), MyHandler)
	print('Started http server')
	server.serve_forever()
    except KeyboardInterrupt:
	print('^C received, shutting down server')
	server.socket.close()

while True:
	time.sleep(0.05)
	
	button.check()
	button1.check()

	# here we are checking timeout queue
	if len(queue) > 0:
		for i in queue:
			i.timeout()

