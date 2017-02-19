import wiringpi
import time

queue = []

class Blinder:

	__PIN_UP = 0
	__PIN_DOWN = 0
	__TIME = 0

	__STIME = 0
	__DIRECTION = "Up" 

	global queue

	def __init__(self, pinup = 0, pindown = 0, time = 0):
		self.__PIN_UP = pinup
		self.__PIN_DOWN = pindown
		self.__TIME = time
		wiringpi.pinMode(self.__PIN_UP,1)
		wiringpi.pinMode(self.__PIN_DOWN,1)
		wiringpi.digitalWrite(self.__PIN_UP,1)
		wiringpi.digitalWrite(self.__PIN_DOWN,1)
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

	def button(self):
		self.addToQueue()

	def timeout(self):
		if (self.__STIME + self.__TIME) < time.time():
			self.addToQueue()
		

class Button:

	__PIN_IN = 0
	__REFOBJ = 0
	__CHANGE = 0
	__TIME = 0
	__CURSTATE = 0 
	__PRVSTATE = 1

	global queue

	def __init__(self, pinin = 0, refobj = 0):
		self.__PIN_IN = pinin
		self.__REFOBJ = refobj
		wiringpi.pinMode(self.__PIN_IN,0)

	def check(self):
		self.__CURSTATE = wiringpi.digitalRead(self.__PIN_IN)
		if self.__CURSTATE != self.__PRVSTATE:
			self.__CHANGE = not self.__CHANGE
			a = time.time()
			tmp = a - self.__TIME
			if self.__CURSTATE < self.__PRVSTATE:
				
				print( __name__ + "Edge: falling "+str(tmp))
			elif self.__CURSTATE > self.__PRVSTATE:
				self.__REFOBJ.button()
				print("Edge: rissing "+str(tmp))
			else:
				print("???")
			self.__TIME = time.time()
			self.__PRVSTATE = self.__CURSTATE
		return

	def report(self):
		print("PIN: "+ self.__PIN_IN)
		print("State: " + self.__CURSTATE)
