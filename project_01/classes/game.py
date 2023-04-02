

"""
--------------------------------------------------------------------------
Game class
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
    - Game()
        - setPatternSize() DONE
            - Sets the number of presses for each pattern
            
        - checkPress(location, pattern_list, press_counter) DONE
            - Checks if the guesser pressed the correct key
            - location is the key pressed
            - pattern_list represents the pattern set by the setter
            - press_counter is the current step in the pattern
        
        - checkWinner(p1_score, p2_score) DONE
            - checks if any player/cpu has reached 10 points
            - p1_score is the score of player 1
            - p2_score is the score of player 2 or the cpu
        
        - guessPattern(guesser, pattern_size, pattern_list) DONE
            - checks if the guesser guessed the whole pattern correctly
            - guesser is an instance of the Guesser class
            - pattern_list is the pattern set by the setter
            - pattern_size is the length of pattern_list
        
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
import sys
import time
import Adafruit_BBIO.PWM as PWM
from random import randint
from guesser import Guesser
from setter import Setter

#gets the path for the drivers
sys.path.append("/var/lib/cloud9/ENGI301/project_01/drivers")
import nav_button as Button
import hd44780 as LCD
import ht16k33 as LED

FIRST_TRELLISLED = 0
LAST_TRELLISLED = 15

MIN_PATTERN_LENGTH = 4
MAX_PATTERN_LENGTH = 10
LCD_COL_SPACE = 2
TIMEOUT_CODE = 9998
TIMEOUT = 15.0

#Constants for the LCD
CURSOR_LEFT_LIMIT = 0
CURSOR_RIGHT_LIMIT = 15
COL_INDEX = 0
ROW_INDEX = 1
ROW_1 = 0
ROW_2 = 1

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
software_debug = False

#Testing individual drivers
button_debug = False
lcd_debug = True

# ------------------------------------------------------------
# Game superclass
# ------------------------------------------------------------
class Game():
    
    lcd = None
    btn_left = None
    btn_right = None
    btn_select = None
    led = None
    #dictionary to map column numbers to the displayed numbers
    pattern_length = {}
    guesser = None
    setter = None
    pattern_size = None
    
    def __init__(self, lcd, btn_left, btn_right, btn_select,led):
        self.lcd = lcd
        self.btn_left = btn_left
        self.btn_right = btn_right
        self.btn_select = btn_select
        self.led = led
        
    def setPatternSize(self):
        """Allows player to set the size of each pattern sequence
            Inputs: None
            Output: The length of the pattern that was set
        """
        # test if the mappng of pattern lengths to column numbers is correct
        if software_debug or button_debug:
            print("Testing setPatternSize")
            print("length of pattern?")
            time.sleep(1)
            cursor = 0
        
        else:
            #displays message on first row of lcd
            self.lcd.clear()
            self.lcd.message("Pattern Length?")
            #sets cursor to 1st col, 2nd row
            self.lcd.setCursor(0,1)
        
        #disiplays the lengths of the patterns (4 to 10) on the lcd
        #maps them to the column numbers in pattern_length
        for p_length in range(MIN_PATTERN_LENGTH, MAX_PATTERN_LENGTH+1):
            
            if software_debug or button_debug:
                #print(p_length)
                self.pattern_length[cursor] = p_length
                cursor += 2
            
            else:
                self.lcd.message(str(p_length))
            
                #maps column number to pattern length
                self.pattern_length[self.lcd.cursor_position[COL_INDEX]] = p_length
            
                #leaves a space before the next number
                self.lcd.setCursor(self.lcd.cursor_position[COL_INDEX] + LCD_COL_SPACE,1)
                
        
        #gets the pattern size from the player
        return(self._selectPatternLength())
    
    
    def _selectPatternLength(self):
        """allow user to scroll lcd or select pattern length
            Inputs: None
            Output: the length of the pattern selected by the user
        """
        print("testing _selectPatternLength")
        
        #resets the cursor position to the first column, second row
        self.lcd.setCursor(CURSOR_LEFT_LIMIT, ROW_2)
        #if no button is pressed within 15 seconds, return the timeout code
        self.idle_time = time.time()

        while(time.time() - self.idle_time  < TIMEOUT):
            
            # test if the column number changes when cursor position is shifted left and right
            if software_debug:
                for cursor in range(12,-2,-LCD_COL_SPACE):
                    print("cursor: {0}, value {1}".format(cursor, self.pattern_length[cursor]))
                    time.sleep(1)
                
                for cursor in range(0,14,LCD_COL_SPACE):
                    print("cursor: {0}, value {1}".format(cursor, self.pattern_length[cursor]))
                    time.sleep(1)
                
                return(6)
            
            #button tests: test if the dictionary can be navigated using buttons
            elif button_debug or lcd_debug:

                if self.btn_left.is_pressed(): #checks if left button is pressed
                    #moves cursor to the left unless it is already at the leftmost column 
                    if self.lcd.cursor_position[COL_INDEX] >= CURSOR_LEFT_LIMIT:
                        self.lcd.setCursor(self.lcd.cursor_position[COL_INDEX] - LCD_COL_SPACE, ROW_2)
                    
                        
                    #prints the pattern size at the cursor position
                    print(self.pattern_length[self.lcd.cursor_position[COL_INDEX]])
                    #displays current pattern position on led
                    self.led.blank()
                    self.led.update(self.pattern_length[self.lcd.cursor_position[COL_INDEX]])
                    
                
                    #resets the idle timer
                    start_idle_time = time.time()
                    time.sleep(0.5)
                    
            
                elif self.btn_right.is_pressed():
                    #moves cursor to the right unless it is already at the leftmost column
                    if self.lcd.cursor_position[COL_INDEX] < 12:
                        self.lcd.setCursor(self.lcd.cursor_position[COL_INDEX] + LCD_COL_SPACE, ROW_2)
                    
                    #prints the pattern size at the cursor position
                    print(self.pattern_length[self.lcd.cursor_position[COL_INDEX]])
                    
                    #displays current pattern position on led
                    self.led.blank()
                    self.led.update(self.pattern_length[self.lcd.cursor_position[COL_INDEX]])
            
                    #resets the idle timer
                    start_idle_time = time.time()
                    time.sleep(0.5)
                
                elif self.btn_select.is_pressed():
                    
                    #prints the pattern size at the cursor position
                    self.pattern_size = self.pattern_length[self.lcd.cursor_position[COL_INDEX]]
                    print(self.pattern_size)
                    self.lcd.clear()
                    self.lcd.setCursor(CURSOR_LEFT_LIMIT, ROW_1)
                    self.lcd.message("Pattern Length:")
                    self.lcd.setCursor(CURSOR_LEFT_LIMIT, ROW_2)
                    self.lcd.message(str(self.pattern_size))
                    time.sleep(0.5)
                    
                    #returns the pattern length that was selected
                    return(self.pattern_size)
        
        #returns the timeout code if idle time exceeds timeout
        if lcd_debug:
            print(TIMEOUT_CODE)
        return (TIMEOUT_CODE)
        
    def _checkPress(self, press_location, current_step, pattern_list):
        """Checks if the guesser pressed the right button in the pattern
            Output: True if the correct button was pressed, False otherwise
        """
        #turns the LED on for 0.5 seconds if the right button was pressed
        if press_location == pattern_list[current_step]:
            if software_debug or lcd_debug:
                print("led {0} is on ".format(press_location))
                self.guesser.trellis.led[press_location] = True
                time.sleep(0.5)
                print("led {0} is off".format(press_location))
                self.guesser.trellis.led[press_location] = False
            
            
            return True
        
        #blinks the led for 2 seconds if the wrong button was pressed
        else:
            if software_debug:
                print("led {0} is blinking".format(press_location))
            else:
                time_counter = time.time()
                while(time.time() - time_counter < 2):
                    self.guesser.trellis.led[press_location] = True
                    time.sleep(0.2)
                    self.guesser.trellis.led[press_location] = False
                    time.sleep(0.2)
            return False
    
    def _checkWinner(self,p1_score, p2_score):
        """Checks if player 1 or player 2/cpu has reached 10 points
            Output: True if any player has reached 10 points, False otherwise
        """
        #prints out the winner on LCD if there is one
        self.lcd.clear()
        self.lcd.setCursor(CURSOR_LEFT_LIMIT, ROW_1)
        if p1_score ==2: 
            if software_debug or lcd_debug:
                print("player 1 is the winner with a score of {0}".format(p1_score))
                
                self.lcd.message("Player 1 wins")
                #turns on the LEDs on the trellis of player 1 for 2 seconds
                if (self.setter != None):
                    self.trellis1.led.fill(True)
                    time.sleep(2)
                    self.trellis1.led.fill(False)
            return True
        
        elif p2_score == 2:
            if software_debug or lcd_debug:
                print("player 2 is the winner with a score of {0}".format(p2_score))
                self.lcd.message("Player 2 wins")
                #turns on the LEDs on the trellis of player 2 for 2 seconds
                if (self.setter != None):
                    self.trellis2.led.fill(True)
                    time.sleep(2)
                    self.trellis2.led.fill(False)
            return True
        
        else:
            if software_debug or lcd_debug:
                print("No winner")
            return False
            
    
    def _guessPattern(self, pattern_size, pattern_list):
        """Checks if the guesser guessed the pattern correctly
            Output: True if the Guesser guessed the pattern correctly, False otherwise
        """
        # displays the pattern to the guesser
        if software_debug or lcd_debug:
            print("\n")
            print("testing showPattern")
        self._showPattern(pattern_size, pattern_list)
        
        if software_debug:
            print("enter pattern")
        else:
            self.lcd.clear()
            self.lcd.setCursor(CURSOR_LEFT_LIMIT, ROW_1)
            self.lcd.message("Enter pattern!")
            self.guesser.trellis.read_buttons()[0]
            time.sleep(0.5)
        #tests a correct pattern
        if software_debug:
            guesser_pattern = pattern_list
            print("simulating the guesser guessing the pattern")
        
        #records and checks each of the guesser's presses
        for press_counter in range(pattern_size):
            
                # records the duration for which the guesser is 'idle'
                start_idle_time = time.time()

                # gets the first button that was pressed and released, incase the user presses multiple buttons at once
                #the list of pressed buttons is the 1st value returned by read_buttons
                pressed_buttons = []
                
                #waits for user press
                while(pressed_buttons == []):
                    time.sleep(0.1)
                    print(pressed_buttons)
                    pressed_buttons = self.guesser.trellis.read_buttons()[0]
                    
                press_location = pressed_buttons[0]
                print(press_location)
                    
                #lights up the pressed button for 0.5 seconds
                self.guesser.trellis.led[press_location] = True
                time.sleep(1)
                self.guesser.trellis.led[press_location] = False
                    
                if(press_location != None):
                    #checks if the button pressed was correct
                    if self._checkPress(press_location, press_counter, pattern_list):
                        # resets the timeout clock
                        if software_debug or lcd_debug:
                            self.lcd.clear()
                            self.lcd.message("press correct")
                            print("press correct, idle timer reset")
                        start_idle_time = time.time()
                        
                    else:
                        if software_debug or lcd_debug:
                            print("Incorrect press!")
                            self.lcd.clear()
                            self.lcd.message("wrong press")
                        return False
                
                # guesser loses the point if no button is pressed for 15 seconds  
                if time.time() - start_idle_time > TIMEOUT:
                    if software_debug or lcd_debug:
                        print("sorry time is up")
                        self.lcd.clear()
                        self.lcd.message("Sorry, time is up")
                    return False
        return True
            
    
    def _showPattern(self, pattern_size, pattern_list):
        """Shows each step in the pattern to the guesser for two seconds
            Output: none
        """
        if software_debug:
            print("\n")
            print("Showing the pattern to the guesser")
            
       #tracks the number of steps of the pattern already shown
        for flash_counter in range(pattern_size):
            if software_debug:
                print("led {0} in position {1} is on".format(flash_counter, pattern_list[flash_counter]))
                time.sleep(0.5)
                #print("led {0} in position {1} is off".format(flash_counter, pattern_list[flash_counter]))
            elif lcd_debug:
                self.guesser.trellis.led[pattern_list[flash_counter]] = True
                print("led {0} in position {1} is on".format(flash_counter, pattern_list[flash_counter]))
            
                time.sleep(2)
                self.guesser.trellis.led[pattern_list[flash_counter]] = False
                
        return
    
    def cleanup(self):
        """ clears LCD display and turns off the LEDs"""
        
        self.lcd.clear()
        self.guesser.led.blank()
        if(self.setter != None):
            self.setter.led.blank()
        
        return

    
# -----------------------------------------------------------------------
# Start of the twoPlayer subclass
# -----------------------------------------------------------------------

    
# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

# -----------------------------------------------------
# Testing for the game class
# ----------------------------------------------------

    #creates the buttons for the button test
    left_btn = Button.Button("P2_18")
    right_btn = Button.Button("P2_20")
    select_btn = Button.Button("P2_22")
    lcd = LCD.LCD(rs, enable, d4, d5, d6, d7, cols, rows)
    led = LED.LED(1, 0x70)
    test_game = Game(lcd,left_btn,right_btn, select_btn, led)
    #TODO: test for setPatternSize and _selectPatternLength
    #print("Testing setPatternSize and _selectPatternLength")
    test_game.setPatternSize()
    #p_list = ["a","b","c","d","e","f"]
    #test_game._guessPattern(6,p_list)
    #test_game._checkWinner(0,0)
    
    # test for _showPattern
    #print("Testing _showPattern")
    #p_length = test_game.setPatternSize()
    #test_game._showPattern(p_length,p_list)
    
    #test for guessPattern, setPatternSize, _showPattern, and checkPress
    #print("Testing guessPattern")
    #test_game.guessPattern(p_length,p_list)
    
    #test for checkWinner
    #print("Testing checkWinner")
    #test_game.checkWinner(10,1) #player 1 wins
    #test_game.checkWinner(1,10) #player 2 wins
    #test_game.checkWinner(1,1) #false
    

