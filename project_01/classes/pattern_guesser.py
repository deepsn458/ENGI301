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

Use the following hardware components to make a programmable combination lock:  
  - HT16K33 Display
  - Button
  - Red LED
  - Green LED
  - Potentiometer (analog input)
  - Servo

Requirements:
  - Hardware:
    - When locked:   Red LED is on; Green LED is off; Servo is "closed"; Display is unchanged
    - When unlocked: Red LED is off; Green LED is on; Servo is "open"; Display is "----"
    - Display shows value of potentiometer (raw value of analog input divided by 8)
    - Button
      - Waiting for a button press should allow the display to update (if necessary) and return any values
      - Time the button was pressed should be recorded and returned
    - User interaction:
      - Needs to be able to program the combination for the “lock”
        - Need to be able to input three values for the combination to program or unlock the “lock”
      - Combination lock should lock when done programming and wait for combination input
      - If combination is unsuccessful, the lock should go back to waiting for combination input
      - If combination was successful, the lock should unlock
        - When unlocked, pressing button for less than 2s will re-lock the lock; greater than 2s will allow lock to be re-programmed

Uses:
  - Libraries developed in class
"""

# to test software
software_debug = False
#to test the hardware
button_debug = True
import sys
import time
import game
import onePlayer
import twoPlayer
import guesser
import setter
import threading

#gets the path for the drivers
sys.path.append("/var/lib/cloud9/ENGI301/project_01/drivers")
import nav_button as Button
import hd44780 as LCD
import ht16k33 as LED

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
    lcd = None
    btn_left = None
    btn_right = None
    btn_select = None
    mode_selected = None
    led = None
    
    def __init__(self, lcd, btn_left, btn_right, btn_select, led):
        """Initialize variables, lcd, and buttons"""
        #TODO: INITIALIZE LCD DISPLAY
        self.lcd = lcd
        self.btn_left = btn_left
        self.btn_right = btn_right
        self.btn_select = btn_select
        self.led = led
    
    def _setup(self):
        """sets up the lcd display
        #TODO: clear lcd display """
        
    
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
                print("1 player")
                
                self.led.blank()
                self.led.text(" P1 ")
                
                time.sleep(0.5)
            
            #scrolls right if the right button is pressed
            elif self.btn_right.is_pressed():
                self.lcd.setCursor(CURSOR_RIGHT_LIMIT, 1)
                print("2 player")
                
                self.led.blank()
                self.led.text(" P2 ")
                
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
#-------------------------------------------------------------
# main script
#------------------------------------------------------------
if __name__ == "__main__":
    # test the getGamemode method with the buttons
    btn_left = Button.Button("P2_18")
    btn_right = Button.Button("P2_20")
    btn_select = Button.Button("P2_22")
    led = LED.LED(1, 0x70)

    
    lcd = LCD.LCD(rs, enable, d4, d5, d6, d7, cols, rows)
    game = patternGuesser(lcd,btn_left,btn_right,btn_select,led)
    print(game.getGamemode())
    
    
    