"""
--------------------------------------------------------------------------
Guesser
--------------------------------------------------------------------------
License:   
Copyright 2021-2023 Deepak Narayan

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
The setter module provides the methods that will manipulate the hardware for the setter
This module is only used in the two player game mode

APIs:
  - Setter(led, trellis)
    - led is an instance of the led class
    - trellis is the instance of the trellis class

    - getLed()
        - returns the setter's led object
    - getTrellis()
        - returns the setter's trellis object
    - updateScore()
        - updates the setter's score
    - getScore()
        - returns the setter's score
"""

# ------------------------------------------------------------------------
# Main Tasks
# ------------------------------------------------------------------------
#Constants for the LCD
CURSOR_LEFT_LIMIT = 0
CURSOR_RIGHT_LIMIT = 15
COL_INDEX = 0
ROW_INDEX = 1
ROW_1 = 0
ROW_2 = 1

FIRST_TRELLISLED = 0
LAST_TRELLISLED = 15

#pins for lcd
rs = "P1_2"
enable = "P1_4"
d4 = "P2_2"
d5 = "P2_4"
d6 = "P2_6"
d7 = "P2_8"
cols = 16
rows = 2

TIMEOUT= 15
TIMEOUT_CODE = 9998
#testing the code without the hardware
software_debug = True

import sys
import time
import game
import random
import guesser
import setter
import busio
import board


import nav_button as Button
import hd44780 as LCD
import ht16k33 as LED
from adafruit_trellis import Trellis
#to test the software
software_debug = True
class Setter():
    trellis = None
    led = None
    score = 0
    def __init__(self, trellis, led):
        self.trellis = trellis
        self.led = led
    #end def
    
    def getLED(self):
        """Returns the setter's led object"""
        return self.led
    # end def
    
    def getTrellis(self):
        """Returns the setter's trellis object"""
        return self.trellis
    # end def
    
    def updateScore(self):
        """ Updates the setter's score"""
        self.score += 1
        self.led.update(self.score)
    # end def
    
    def getScore(self):
        """Returns the setter's score"""
        return self.score
        
    # end def
    
    def setPattern(self, pattern_size, lcd):
        """Allows the setter to set a pattern for the guesser to guess
           Output: The pattern that was set. The timeout code is retured if the game times out"""
        
        print("testing setPattern")
        time.sleep(0.5)
        # list to store the pattern
        pattern_list = []
        
        #keeps track of the current pattern count
        pattern_count = 0
         # stores the duration for which the setter is idle
        idle_time = time.time()
        lcd.clear()
        lcd.message("Set Pattern!")
        # if the setter does not press a button in 15 seconds, return the timeout code
        while(time.time() - idle_time < TIMEOUT):
            print("pattern_count = {0}, pattern_size = {1}".format(pattern_count, pattern_size))
            # checks if the nested loop was completed successfully and breaks the while loop
            if pattern_count == pattern_size:
                break
            # Adds the required number of steps to the pattern
            while(pattern_count < pattern_size):
                time.sleep(0.5)
                
                self.trellis.read_buttons()[0]
                print("select the {0}th LED".format(pattern_count))
            
                #waits for a button to be pressed
                
                #gets the first button that was pressed and released by the setter
                pressed_buttons = []
                #waits for the user press
                while(pressed_buttons == []):
                    time.sleep(0.1)
                    print(pressed_buttons)
                    pressed_buttons = self.trellis.read_buttons()[0]
                    
                    if (time.time() - idle_time > TIMEOUT):
                        print("sorry timeout!")
                        return list([TIMEOUT_CODE])
                    
                #adds the pressed button to the list and flashes the corresponding led for 0.5s
                pattern_list.append(pressed_buttons[0])
                print(pressed_buttons[0])
                self.trellis.led[pressed_buttons[0]] = True
                time.sleep(0.5)
                self.trellis.led[pressed_buttons[0]] = False
                
                # displays how many steps the setter has set in the pattern
                self.led.update(pattern_count+1)
                
                #resets the idle timer and adds 1 to the pattern count
                idle_time = time.time()
                print("idle timer reset!")
                pattern_count += 1
        lcd.clear()
        print(pattern_list)
        return pattern_list
    # end def
# end class
# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------
if __name__ == "__main__":
    lcd = LCD.LCD(rs, enable, d4, d5, d6, d7, cols, rows)
    led1 = LED.LED(1,0x70)
    
    # Create the I2C interface
    i2c = busio.I2C(board.SCL_2, board.SDA_2)
    trellis_1 = Trellis(i2c)
    s1 = Setter(trellis_1,led1)
    s1.setPattern(4,lcd)