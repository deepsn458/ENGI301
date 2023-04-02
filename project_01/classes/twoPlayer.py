
"""
--------------------------------------------------------------------------
twoPlayer class
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
APIs:
    -TwoPlayer(Game)
            - - pins for led, buttons, trellis, lcd are passed as input
            - setup()
                - sets up the hardware for the two player game mode
            
            - run()
                - runs the two player game mode
            
            - playTwoPlayer(pattern_length)
                - runs the actual game for the two player mode
                - pattern_length is the length of pattern_list
            
            - chooseGuesser(trellis1, trellis2, led1, led2)
                - randomely chooses which player will be the guesser and which will be the setter
                - trellis 1 and 2 are the keypad/led matrices for player 1 and 2 respectives
                - led1 and 2 are the led displays for player 1 and 2 respectively
            
            - swap(guesser, setter)
                - swaps the guesser and setter after each game
    --------------------------------------------------------------------------

"""
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

class twoPlayer(game.Game):
    trellis1 = None
    trellis2 = None
    led1 = None
    led2 = None
    pattern_size = 0
    #stores the pattern set by the setter
    pattern_list = []
    
    #stores the guesser and setter
    guesser = None
    setter = None
    
    def __init__(self,lcd,btn_left,btn_right,btn_select, led1, led2, trellis1, trellis2):
        game.Game.__init__(self,lcd, btn_left, btn_right, btn_select,led1)
        
        self.trellis1 = trellis1
        self.trellis2 = trellis2
        self.led1 = led1
        self.led2 = led2
        
        self._setup()
    
    def _setup(self):
        """clears the LCD and Trellises. Prints 0 on LEDs"""
        if software_debug:
            print("testing setup")
            print("")
            time.sleep(1)
        else:
            self.lcd.clear()
            self.trellis1.clear()
            self.trellis2.clear()
            self.led1.update(0)
            self.led2.update(0)
        return
    
    def run(self):
        """ Runs the twoPlayer game mode"""
        self.lcd.clear()
        # the main logic for the two player game mode
        self.playTwoPlayer(self.setPatternSize())
        time.sleep(2)
        #calls the cleanup methpod
        self.cleanup()
    
    def playTwoPlayer(self, pattern_size):
        """ The main logic for the two player game mode
            Output: nothing
        """
        # choose the guesser and setter to start the game
        self._chooseGuesser()
        
        
        # setter will choose the pattern
        #self.setter.setPattern(pattern_size,self.lcd)
        
        #makes sure the players' scores are not swapped when the guesser and setter are swapped
        p1_score = 0
        p2_score = 0
        
            
        #play the game until there is a winner
        while (not self._checkWinner(p1_score, p2_score)):
            # setter will choose the pattern
            print(p1_score, p2_score)
            self.pattern_list = self.setter.setPattern(pattern_size, self.lcd) 
        
            # if there is a timeout, give the guesser a point
            if TIMEOUT_CODE in self.pattern_list:
                self.guesser.updateScore()
            
            time.sleep(2)
            # prints the scores on the players' lcds
            self.guesser.led.update(self.guesser.score)
            self.setter.led.update(self.setter.score)
            #otherwise the guesser will try guessing the pattern
            # if the guesser guesses the pattern correctly, add a point
            # otherwise, give the setter a point
            if self._guessPattern(pattern_size, self.pattern_list):
                self.lcd.clear()
                self.lcd.message("guesser is right!")
                self.guesser.updateScore()
            else:
                self.lcd.clear()
                self.lcd.message("guesser is wrong!")
                self.setter.updateScore()
            time.sleep(2)
            
             # updates the score of each player
            if self.setter.trellis == self.trellis1:
                p1_score = self.setter.score
                p2_score = self.guesser.score
            else:
                p1_score = self.guesser.score
                p2_score = self.setter.score
            
            #displays the scores of the players
            self.lcd.clear()
            self.lcd.setCursor(CURSOR_LEFT_LIMIT,ROW_1)
            self.lcd.message("P1:")
            self.lcd.setCursor(CURSOR_LEFT_LIMIT+4, ROW_1)
            self.lcd.message(str(p1_score))
            
            self.lcd.setCursor(CURSOR_LEFT_LIMIT,ROW_2)
            self.lcd.message("P2:")
            self.lcd.setCursor(CURSOR_LEFT_LIMIT+4, ROW_2)
            self.lcd.message(str(p2_score))
            
            time.sleep(2)
            #swaps the players
            self._swap()
            self.lcd.clear()
            self.lcd.setCursor(CURSOR_LEFT_LIMIT,ROW_1)
            self.lcd.message("swap!")
            time.sleep(2)
            
             
            print("setter score is {0}, guesser score is {1}".format(self.setter.score, self.guesser.score))   
            print("p1_score is {0} p2_score is {1}".format(p1_score, p2_score))
        return
        
    def _swap(self):
        """ Swaps the setter and guesser for the next round
            Output: nothing
        """
        #test the swapping operator
        print("guesser: {0}, setter: {1}".format(self.guesser.trellis,self.setter.trellis))
        #temporary variables to execute the swap
        temp_trellis = self.setter.trellis
        temp_led = self.setter.led
        temp_score = self.setter.score
        self.setter = setter.Setter(self.guesser.trellis, self.guesser.led)
        self.setter.score = self.guesser.score
            
        self.guesser = guesser.Guesser(temp_trellis, temp_led)
        self.guesser.score = temp_score
            
        print("guesser: {0}, setter: {1}".format(self.guesser.trellis,self.setter.trellis))
    
    
    def _chooseGuesser(self):
        """ Randomely chooses which player will set the pattern and which player will guess the pattern
            Output: a Guesser object and a Setter object
        """
        # if a 1 is randomely generated, the player with trellis1 and led1 is made the setter
        # otherwise the player with trellis2 and led2 is made the setter
        print("testing _chooseGuesser")
        time.sleep(0.5)
        if random.randint(1,2) == 1:
            self.setter = setter.Setter(self.trellis1, self.led1)
            self.guesser = guesser.Guesser(self.trellis2, self.led2)
            print(self.guesser.trellis)
    
        else:
            self.setter = setter.Setter(self.trellis2, self.led2)
            self.guesser = guesser.Guesser(self.trellis1, self.led1)
            print(self.guesser.trellis)
        self.guesser.led.text("GUES")
        self.setter.led.text("SET")
    
        

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    #test for _chooseGuesser
    left_btn = Button.Button("P2_18")
    right_btn = Button.Button("P2_20")
    select_btn = Button.Button("P2_22")
    lcd = LCD.LCD(rs, enable, d4, d5, d6, d7, cols, rows)
    led1 = LED.LED(1,0x70)
    led2 = LED.LED(1,0x71)
    
    # Create the I2C interface
    i2c = busio.I2C(board.SCL_2, board.SDA_2)
    trellis_1 = Trellis(i2c)
    trellis_2 = Trellis(i2c,[0x71])
    test_p2 = twoPlayer(lcd,left_btn,right_btn,select_btn,led1, led2, trellis_1, trellis_2)
    test_p2.run()