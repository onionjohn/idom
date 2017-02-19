#!/usr/bin/python

import wiringpi
import time

from objects import *

global queue

wiringpi.wiringPiSetup()

roleta = Blinder(0,2,3)
roleta1 = Blinder(6,3,6)
button = Button(7, roleta)
button1 = Button(10, roleta1)

while True:
	time.sleep(0.05)
	
	button.check()
	button1.check()

	# here we are checking timeout queue
	if len(queue) > 0:
		for i in queue:
			i.timeout()
