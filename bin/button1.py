#!/usr/bin/python

import wiringpi
import time

PS=1
CT = time.time()
RS0 = 1
RS1 = 0

cnt = 0

wiringpi.wiringPiSetup()
wiringpi.pinMode(7,0)
wiringpi.pinMode(2,1)
wiringpi.pinMode(0,1)
wiringpi.digitalWrite(2,1)
wiringpi.digitalWrite(0,0)

while True:
	time.sleep(0.05)
	CS = wiringpi.digitalRead(7)
	if CS != PS:
		tmp = time.time() - CT
		if CS < PS:
			print("opadaniei "+str(tmp))
		elif CS > PS:
			print("wznoszenie "+str(tmp))
			cnt = cnt + 1
			if cnt%3 == 0:
				print "00"
				wiringpi.digitalWrite(2, 1)
				wiringpi.digitalWrite(0, 1)
			elif cnt%3 == 1:
				print "01"
				wiringpi.digitalWrite(2, 0)
				wiringpi.digitalWrite(0, 1)
			elif cnt%3 == 2:
				print "10"
				wiringpi.digitalWrite(2, 1)
				wiringpi.digitalWrite(0, 0)
		else:
			print("???")
		PS = CS 
		CT = time.time()
