"""
--------------------------------------------------------------------------
Pattern Guessing Game
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
Software API:
    
    patternGuesser()
     This class is used to run the pattern Guesser game. It will be used to determine the specific
     game mode selected by the user and then initialize a one player or two player game accordingly
     
        _setup():
            - clears the LCD display
        
        run():
            - runs the main logic for the game
        
        getGamemode():
            - Returns the game mode selected by the user (either one player or two player)
        
        _cleanup():
            - Turns off all the hardware

--------------------------------------------------------------------------
Background Information: 
 
  * Uses HD44780U 16x02 LCD Display
        
  * Uses 7-segment LED with HT16K33 I2C Backpack
     
    
  * Uses Adafruit Trellis with Adafruit's Circuit Python Trellis Library
        * https://github.com/adafruit/Adafruit_CircuitPython_Trellis
    
    
--------------------------------------------------------------------------------
    
"""

import sys
import time


import game
import onePlayer
import twoPlayer
import guesser
import setter
import busio
import board

import nav_button as Button
import hd44780 as LCD
import ht16k33 as LED
from adafruit_trellis import Trellis
# ---------------------------------------------------
# Constants
# ---------------------------------------------------
CURSOR_LEFT_LIMIT = 0
CURSOR_RIGHT_LIMIT = 15
LCD_COLS = 16
LCD_ROWS = 2
ROW_1 = 0
ROW_2 = 1
COL_INDEX = 0
ROW_INDEX = 0

# ---------------------------------------------------------
#pin assignments
# --------------------------------------------------------
#pins for lcd
rs = "P1_2"
enable = "P1_4"
d4 = "P2_2"
d5 = "P2_4"
d6 = "P2_6"
d7 = "P2_8"
cols = 16
rows = 2


class patternGuesser():
    """ Pattern Guesser """
    lcd = None
    btn_left = None
    btn_right = None
    btn_select = None
    led1 = None
    led2 = None
    trellis1 = None
    trellis2 = None
    mode_selected = None
    
    def __init__(self,lcd, btn_left, btn_right, btn_select, 
                       led1,led2,trellis1,trellis2):
        """Initialize variables, lcd, and buttons"""
        #TODO: INITIALIZE LCD DISPLAY
        self.lcd = lcd
        self.btn_left = btn_left
        self.btn_right = btn_right
        self.btn_select = btn_select
        self.led1= led1
        self.led2 = led2
        self.trellis1 = trellis1
        self.trellis2 = trellis2
        self._setup()
        
        #end def
    
    def _setup(self):
        """sets up the lcd display"""
        self.lcd.clear()
        
        #end def
        
    def run(self):
        """ The main logic for the game """
        # initializes and runs the one player or two player game depending on the user's input\
        
        #if true, run the one player game mode
        if self.getGamemode():
            game = onePlayer.onePlayer(self.lcd, self.btn_left, self.btn_right, self.btn_select,
                                        self.led1, self.trellis1)
        else:
            game = twoPlayer.twoPlayer(self.lcd, self.btn_left, self.btn_right, self.btn_select,
                                        self.led1, self.led2, self.trellis1, self.trellis2)
         
        game.run()
        
        self._cleanup()
        
        #end def
        
        
    def getGamemode(self):
        """Checks whether the user wants to play single player or TwoPlayer
            Outputs: True if 1 player mode is selected
                     False if 2 player mode is selected
        """
        # Display the options on the lcd display
        self.gamemodes = {CURSOR_LEFT_LIMIT:'1 player', CURSOR_RIGHT_LIMIT:'2 player'}
        #shows "choose mode" on the first row of the lcd
        self.lcd.setCursor(CURSOR_LEFT_LIMIT, ROW_1)
        self.lcd.clear()
        self.lcd.message("Choose Mode")
        
        #shows the player 1 and player 2 options on the lcd
        self.lcd.setCursor(CURSOR_LEFT_LIMIT, ROW_2)
        self.lcd.message("1 player")
        self.lcd.setCursor(CURSOR_LEFT_LIMIT+8, ROW_2)
        self.lcd.message("2 player")
        
        #reset the cursor to the 2nd row so the modes can be selected
        self.lcd.setCursor(CURSOR_LEFT_LIMIT,ROW_2)
        
        # checks which button is pressed
        while(True):
            #scrolls left if the left button is pressed and shows the gamemode on the led
            if self.btn_left.is_pressed():
                self.lcd.setCursor(CURSOR_LEFT_LIMIT,1)
                
                self.led1.blank()
                self.led1.text(" P1 ")
                
                time.sleep(0.5)
            
            #scrolls right if the right button is pressed
            elif self.btn_right.is_pressed():
                self.lcd.setCursor(CURSOR_RIGHT_LIMIT, 1)
                print("2 player")
                
                self.led1.blank()
                self.led1.text(" P2 ")
                
                time.sleep(0.5)
                
            #gets the current cursor position and returns the corresponding game mode and shows the led on the game mode
            elif self.btn_select.is_pressed():
                #If the cursor position is on player 1, return true
                if self.lcd.cursor_position[COL_INDEX] == CURSOR_LEFT_LIMIT:
                    print(self.gamemodes[self.lcd.cursor_position[COL_INDEX]])
                    
                    self.lcd.clear()
                    self.lcd.message("1 player")
                    return True
                
                else:
                    #if cursor position is on player 2, return false
                    self.lcd.clear()
                    self.lcd.message("2 player")
                    return False
    #end def
    
    def _cleanup(self):
        """ Cleans up the hardware, turning everything off """
        self.lcd.setCursor(CURSOR_LEFT_LIMIT, ROW_1)
        self.lcd.message("Good Game!")
        time.sleep(2)
        self.lcd.clear()
        self.trellis1.led.fill(False)
        self.trellis2.led.fill(False)
        self.led1.blank()
        self.led2.blank()
    #end def

#end class

#-------------------------------------------------------------
# main script
#------------------------------------------------------------
if __name__ == "__main__":
    # test the getGamemode method with the buttons
    btn_left = Button.Button("P2_18")
    btn_right = Button.Button("P2_20")
    btn_select = Button.Button("P2_22")
    led1 = LED.LED(1, 0x70)
    led2 = LED.LED(1, 0x71)
    
    # Create the I2C interface
    i2c = busio.I2C(board.SCL_2, board.SDA_2)
    trellis1 = Trellis(i2c)
    trellis2 = Trellis(i2c, [0x71])
    lcd = LCD.LCD(rs, enable, d4, d5, d6, d7, cols, rows)
    pattern_guesser = patternGuesser(lcd,btn_left,btn_right,btn_select,led1,led2, trellis1, trellis2)
    pattern_guesser.run()
    
    
    