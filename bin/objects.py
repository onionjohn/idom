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
		
