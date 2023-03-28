"""
--------------------------------------------------------------------------
HT16K33 I2C Library
--------------------------------------------------------------------------
License:   
Copyright 2018-2023 <NAME>

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
Software API:

  Trellis(bus, address=0x70)
    - Provide i2c bus that dispaly is on
    - Provide i2c address for the display
    
    clear()
      - Turn off all the LEDs
    
    readPress()
    - Checks if a key was pressed
    - Returns the location of the key that was pressed, None if no key was pressed
   
    
    setLed(led)
    - Turns on the specified led
    
    clearLed(led)
    - turns off the specified led
    
    writeDisplay()
    - Writes the specific change to the led state to the trellis
    
  
--------------------------------------------------------------------------
Background Information: 
 
    * Base code (adapted below):
        * https://github.com/tdicola/Adafruit_Trellis_Python/blob/master/Adafruit_Trellis.py
        # This is a library for the Adafruit Trellis w/HT16K33
#
#   Designed specifically to work with the Adafruit Trellis 
#   ----> https://www.adafruit.com/products/1616
#   ----> https://www.adafruit.com/products/1611
#
#   These displays use I2C to communicate, 2 pins are required to  
#   interface
#   Adafruit invests time and resources providing this open source code, 
#   please support Adafruit and open-source hardware by purchasing 
#   products from Adafruit!
#
#   Written by Limor Fried/Ladyada for Adafruit Industries.  
   
        
"""
import Adafruit_GPIO.I2C as I2C
import time
# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------
lED_ON = 1
LED_OFF = 0
HT16K33_BLINK_CMD = 0x80
HT16K33_BLINK_DISPLAYON = 0x01
HT16K33_BLINK_OFF = 0
HT16K33_BLINK_2HZ = 1
HT16K33_BLINK_1HZ = 2
HT16K33_BLINK_HALFHZ  = 3
HT16K33_CMD_BRIGHTNESS = 0xE0
HT16K33_BRIGHTNESS_MAX = 0x0F
HT16K33_BRIGHTNESS_MIN = 0x00

led_array =  [ 0x3A, 0x37, 0x35, 0x34, 
			0x28, 0x29, 0x23, 0x24, 
			0x16, 0x1B, 0x11, 0x10, 
			0x0E, 0x0D, 0x0C, 0x02 ]

button_array = [ 0x07, 0x04, 0x02, 0x22,
			  0x05, 0x06, 0x00, 0x01,
			  0x03, 0x10, 0x30, 0x21,
			  0x13, 0x12, 0x11, 0x31 ]

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------
class Trellis():
	""" Class to manage an Adafruit Trellis 4x4 keypad and led matrix """
	#class variables
	bus = None
	address = None
	location = None
	def __init__(self,bus, address=0x70):
		"""Create a Trellis object."""
		self.displaybuffer = [0]*8
		self._keystate = [0]*6 #the previous state ofi 
		self._prevstate = [0]*6
		self._i2c = I2C.Device(address, bus)
		self._i2c.writeList(0x21, []) # Turn on the oscillator.
		self.blinkRate(HT16K33_BLINK_OFF)
		self.setBrightness(HT16K33_BRIGHTNESS_MAX) # Max brightness.
		self._i2c.writeList(0xA1, []) # Turn on interrupt, active high.'
		
	def writeDisplay(self):
		"""Write the LED display buffer values to the hardware."""
		self._check_i2c()
		data = []
		for buf in self.displaybuffer:
			data.append(buf & 0xFF)
			data.append(buf >> 8)
		#self._i2c.writeList(0, data)
		
	def blinkRate(self, b):
		"""Set the blink rate to the provided value.
		   Value should be an integer 0 to 3--values outside that range will default
		   to 0.
		"""
		self._check_i2c()
		b = 0 if b > 3 else b # turn off if not sure
		b = 0 if b < 0 else b
		self._i2c.writeList(HT16K33_BLINK_CMD | HT16K33_BLINK_DISPLAYON | (b << 1), [])
	
	def setLED(self, led):
		"""Turn on the specified LED in the display buffer."""
		if led > 16 or led < 0: return  
		self.displaybuffer[led_array[led] >> 4] |= (1 << (led_array[led] & 0x0F))

	def clearLED(self, led):
		"""Turn off the specified LED in the display buffer."""
		if led > 16 or led < 0: return
		self.displaybuffer[led_array[led] >> 4] &= ~(1 << (led_array[led] & 0x0F))	
	
	def clear(self):
		"""Clear all the LEDs in the display buffer."""
		self.displaybuffer = [0,0,0,0,0,0,0,0]

	def readPress(self):
		#Read the state of the buttons from the hardware Returns the location of the key that was pressed, None if no key was pressed
		self._check_i2c()
		self._prevstate = self._keystate
		self._keystate = self._i2c.readList(0x40, 6)
		
		#checks if any key was pressed
		if any(map(lambda keystate, prevstate: keystate != prevstate, self._keystate, self._prevstate)):
			for key in range(17):
				
				#checks which key was pressed
				if self_keystate[button_array[key] >> 4] & (1 << (button_array[key] & 0X0F)) > 0: 
					return key
		
		else:
			return None
	
	def blinkLED(self, count,led):
		""" blinks the led the specified number of times"""
		for i in range(count):
			self.setLED(led)
			self.writeDisplay()
			
			time.sleep(0.2)
			self.clearLED(led)
			self.writeDisplay()
			
			
	def _check_i2c(self):
		assert self._i2c is not None, 'begin() must be called first!'

	

# End class


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------
if __name__ == '__main__':
	import time
	trellis0 = Trellis(1, 0x70)
	
	# turns on leds
	for i in range(16):
		trellis0.setLED(i)
		trellis0.writeDisplay()
	
	
	#turns off leds
	for i in range(16):
		trellis0.clearLED(i)
		trellis0.writeDisplay()
		
	
	#checks if readpress() works correctly
	press_count = 0
	
	while (press_count < 16):
		btn_pressed = trellis0.readPress()
		
		if btn_pressed != None: #checks if a button has been pressed
			trellis0.setLED(btn_pressed)
			trellis0.writeDisplay()
			press_count += 1
		print("led {0} is on".format(btn_pressed))
		time.sleep(1)
			
	
	while (press_count >= 0):
		btn_pressed = trellis0.readpress()
		
		if btn_pressed != None: #checks if a button has been pressed
			trellis0.clearLED(btn_pressed)
			trellis0.writeDisplay()
			press_count -= 1
		print("led {0} is off".format(btn_pressed))
		time.sleep(1)
			
	
	