#!/usr/bin/python

import wiringpi
import time

from objects import Blinder

PS=1
CT = time.time()
RS0 = 1
RS1 = 0

cnt = 0
queue = []

wiringpi.wiringPiSetup()
wiringpi.pinMode(7,0)
wiringpi.pinMode(2,1)
wiringpi.pinMode(0,1)
wiringpi.digitalWrite(2,1)
wiringpi.digitalWrite(0,1)

roleta = Blinder(0,2,10)

while True:
	time.sleep(0.05)
	CS = wiringpi.digitalRead(7)
	if CS != PS:
		print("")
		if CS < PS:
			print("Edge: falling ")
		elif CS > PS:
			roleta.addToQueue()
			print("Edge: rissing ")
		else:
			print("???")
		PS = CS 
		CT = time.time()
	if len(queue) > 0:
		for i in range(0, len(queue)):
			queue[i].timeout()

