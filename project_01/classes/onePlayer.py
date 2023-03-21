"""
--------------------------------------------------------------------------
onePlayer class
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
 - OnePlayer(Game)
            - pins for led, buttons, trellis, lcd are passed as input
            - setup()
                - sets up the hardware for the one player game mode
            
            - run()
                - runs the one player game mode
            
            - playOnePlayer(pattern_length)
                - runs the actual game for the one player mode
                - pattern_length is the length of pattern_list
            
            -cleanup()
                - returns all hardware to default state
--------------------------------------------------------------------------------------------
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

#testing the code without the hardware
software_debug = True

#Testing individual drivers
button_debug = False
lcd_debug = True

import sys
import time
import game
import random
import guesser 

#gets the path for the drivers
sys.path.append("/var/lib/cloud9/ENGI301/project_01/drivers")
import nav_button as Button
import hd44780 as LCD
import ht16k33 as LED


class onePlayer(game.Game):
    trellis = None
    pattern_size = 0
    cpu_score = 0
    #stores the randomely set pattern
    pattern_list = []
    guesser = None
        
    def __init__(self,lcd,btn_left,btn_right,btn_select,led, trellis):
        game.Game.__init__(self,lcd,btn_left,btn_right,btn_select,led)
        self.trellis = trellis
        self.led = led
            
        self._setup()
            
    def _setup(self):
        """clears the LCD and Trellis. Prints 0 on LED"""
        if software_debug:
            print("testing setup")
            print("")
            time.sleep(1)
        else:
            self.lcd.clear()
            self.trellis.clear()
            self.led.update(0)
        
    def run(self):
        """ Runs the onePlayer game mode"""
        #gets the pattern size
        self.lcd.clear()
        pattern_size = self.setPatternSize()
            
        # the main logic for the one player game mode
        self.playOnePlayer(pattern_size)
            
        #calls the cleanup methpod
        self.cleanup()
        return
            
        
    def playOnePlayer(self, pattern_size):
        """The main logic for the one player game mode
            Output: nothing
        """
        self.lcd.clear()
        self.led.clear()
        self.lcd.setCursor(CURSOR_LEFT_LIMIT,ROW_1)
        #Initialize the guesser
        self.guesser = guesser.Guesser(1,self.led)
        # initialize the scores of the guesser and the cpu
        #if testing software, guesser class is not yet integrated
        
        self.guesser.score = 0
        self.cpu_score = 0
        
        # generate a random pattern  
        self._generatePattern(pattern_size)
        
        #plays the game until the player or cpu reaches 10 points
        while(not self._checkWinner(self.guesser.score, self.cpu_score)):
            #adds 1 to the player's score if the guesser guesses the score correctly
            #otherwise 1 is added to cpu's score
            if self._guessPattern(pattern_size, self.pattern_list):
                self.guesser.score += 1
                #self.led.update(self.guesser.score)
                
                if software_debug or lcd_debug:
                    self.lcd.message("guesser is right")
                    print("guesser got the pattern right!")
                
            else:
                self.cpu_score +=1
                if software_debug or lcd_debug:
                    self.lcd.message("guesser is wrong")
                    print("guesser got the pattern wrong")
            # generate a random pattern for the next round in the game       
            self._generatePattern(pattern_size)
         
        print("onePlayer game doen")   
        return
        
    def _generatePattern(self,pattern_size):
        """Generates the pattern for the CPU
           Output: nothing
        """
        self.pattern_list = []
        for current_step in range(pattern_size):
            self.pattern_list.append(random.randint(FIRST_TRELLISLED, LAST_TRELLISLED))
        
        if software_debug:
            print(self.pattern_list)
        return
# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------
if __name__ == '__main__':
    left_btn = Button.Button("P2_18")
    right_btn = Button.Button("P2_20")
    select_btn = Button.Button("P2_22")
    lcd = LCD.LCD(rs, enable, d4, d5, d6, d7, cols, rows)
    led = LED.LED(1,0x70)
    test_p1 = onePlayer(lcd,left_btn,right_btn,select_btn,led, 2)
    #TODO: test for run
    #TODO: test for _generatePattern
    print("testing generatePattern")
    #test_p1._generatePattern(test_p1.setPatternSize())

    #TODO: test for playOnePlayer
    print("testing playOnePlayer")
    test_p1.playOnePlayer(test_p1.setPatternSize())
    print("Test done")