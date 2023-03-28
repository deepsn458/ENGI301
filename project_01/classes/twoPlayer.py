
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
    
    def __init__(self,lcd,btn_left,btn_right,btn_select, trellis1, trellis2, led1, led2):
        game.Game.__init__(self,lcd, btn_left, btn_right, btn_select)
        
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
        #gets the pattern size
        pattern_size = self.setPatternSize()
            
        # the main logic for the two player game mode
        self.playTwoPlayer(pattern_size)
            
        #calls the cleanup methpod
        self.cleanup()
    
    def playTwoPlayer(self, pattern_size):
        """ The main logic for the two player game mode
            Output: nothing
        """
        # choose the guesser and setter to start the game
        self._chooseGuesser()
        
        
        # setter will choose the pattern
        self.setter.setPattern(pattern_size,self.lcd)
        
        #makes sure the players' scores are not swapped when the guesser and setter are swapped
        p1_score = 0
        p2_score = 0
        
        if not software_debug:
            guesser_score = 0
            setter_score = 0
            
        #play the game until there is a winner
        while (not self._checkWinner(p1_score, p2_score)):
            # setter will choose the pattern
            print(p1_score, p2_score)
            self.pattern_list = self.setter.setPattern(pattern_size, self.lcd) 
        
            # if there is a timeout, give the guesser a point
            if TIMEOUT_CODE in self.pattern_list:
                self.guesser.updateScore()
            
            #otherwise the guesser will try guessing the pattern
            # if the guesser guesses the pattern correctly, add a point
            # otherwise, give the setter a point
            if self._guessPattern(pattern_size, self.pattern_list):
                if software_debug:
                    print("guesser gets a point")
                    self.guesser.updateScore()
                else:
                    self.guesser.updateScore()
            else:
                if software_debug:
                    print("setter gets a point")
                else:
                    self.setter.updateScore()
            
            #swaps the players
            self._swap()
            
            # checks which player is player 1 and which is player 2
            if self.setter.trellis == self.trellis1:
                p1_score = self.setter.score
                p2_score = self.guesser.score
            else:
                p1_score = self.guesser.score
                p2_score = self.setter.score
             
            print("setter score is {0}, guesser score is {1}".format(self.setter.score, self.guesser.score))   
            print("p1_score is {0} p2_score is {1}".format(p1_score, p2_score))
        return
        
    def _swap(self):
        """ Swaps the setter and guesser for the next round
            Output: nothing
        """
        #test the swapping operator
        print("Testing Swap")
        if not software_debug:
            a = 2
            b = 5
            print("a: {0}, b: {1}".format(a,b))
            a, b = b, a
            print("a: {0}, b: {1}".format(a,b))
            
        else:
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
        return
    
    
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
    
         
            self.setter = setter.Setter(self.trellis2, self.led2)
            self.guesser = guesser.Guesser(self.trellis1, self.led1)
            print(self.guesser.trellis)
    
        

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    #test for _chooseGuesser
    test_p2 =twoPlayer(1,2,3,4,5,6,7,8)
    test_p2.run()