#!/usr/bin/python

import wiringpi
import time

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

class Blinder:

	__PIN_UP = 0
	__PIN_DOWN = 0
	__TIME = 0

	__STIME = 0
	__DIRECTION = "Up" 

	def __init__(self, pinup = 0, pindown = 0, time = 0):
		self.__PIN_UP = pinup
		self.__PIN_DOWN = pindown
		self.__TIME = time
		return

	def addToQueue(self):
		if self in queue:
			self.__stopMove()
			queue.remove(self)
		else:
			queue.append(self)
			self.__STIME = time.time()
			if self.__DIRECTION == "Up":
				self.__moveUp()
			else:
				self.__moveDown()
			
		return

	def __moveUp(self):
		wiringpi.digitalWrite(self.__PIN_UP, 0)
		wiringpi.digitalWrite(self.__PIN_DOWN, 1)
		return

	def __moveDown(self):
                wiringpi.digitalWrite(self.__PIN_UP, 1)
                wiringpi.digitalWrite(self.__PIN_DOWN, 0)
		return

	def __stopMove(self):
		if self.__DIRECTION == "Up":
			self.__DIRECTION = "Down"
		else:
			self.__DIRECTION = "Up"

                wiringpi.digitalWrite(self.__PIN_UP, 1)
                wiringpi.digitalWrite(self.__PIN_DOWN, 1)
                return

	def timeout(self):
		if (self.__STIME + self.__TIME) < time.time():
			self.addToQueue()
		


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

