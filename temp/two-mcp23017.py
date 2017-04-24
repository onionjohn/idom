# Turns on each pin of an mcp23017 on address 0x20 ( quick2wire IO expander )
import wiringpi
import time

pin_base = 65
i2c_addr = 0x27
i2c_addr_2 = 0x26
#pins = [65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80]

wiringpi.wiringPiSetup()
wiringpi.mcp23017Setup(pin_base,i2c_addr)
wiringpi.mcp23017Setup(pin_base+16,i2c_addr_2)

#for pin in pins:
for pin in range(65,97):
	print pin
	wiringpi.pinMode(pin,1)
	wiringpi.digitalWrite(pin,1)



raw_input('enter')
for pin in range(65,97):
	print pin
	wiringpi.pinMode(pin,1)
	wiringpi.digitalWrite(pin,0)
	time.sleep(1)
	wiringpi.digitalWrite(pin,1)

