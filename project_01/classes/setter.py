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
TIMEOUT_CODE = 9998
TIMEOUT = 15.0


import random
import time
#to test the software
software_debug = True
class Setter():
    trellis = None
    led = None
    score = 0
    
    def __init__(self, trellis, led):
        self.trellis = trellis
        self.led = led
    
    def getLED(self):
        return self.led
    
    def getTrellis(self):
        return self.trellis
    
    def updateScore(self):
        self.score += 1
    
    def getScore(self):
        return self.score
    
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
        # if the setter does not press a button in 15 seconds, return the timeout code
        while(time.time() - idle_time < TIMEOUT):
            
            # checks if the nested loop was completed successfully and breaks the while loop
            if pattern_count == pattern_size:
                break
            # Adds the required number of steps to the pattern
            while(pattern_count < pattern_size):
                time.sleep(0.5)
                if software_debug:
                    print("select the {0}th LED".format(pattern_count))
                else:
                    lcd.setCursor(0,0)
                    lcd.message("Select the ith LED")
            
                if software_debug:
                    print("led {0} is pressed".format(pattern_count))
                    pattern_list.append(random.randint(1,10))
            
                else:
                    #waits for an led to be pressed
                    while (trellis.readPress() == None):
                        if (time.time() - idle_time < TIMEOUT):
                            print("sorry timeout!")
                            return list([TIMEOUT_CODE])
                    
                    #Turns on the pressed LED for 0.5 seconds and stores it in the list
                    pressed_led = self.trellis.readPress()
                    self.trellis.setLED(pressed_led)
                    self.trelllis.writeDisplay()
                
                    time.sleep(0.5)
                    self.trellis.clearLED(pressed_led)
                    self.trellis.writeDisplay()
                
                    pattern_list.append(pressed_led)
                
                #resets the idle timer and adds 1 to the pattern count
                idle_time = time.time()
                print("idle timer reset!")
                pattern_count += 1
        
        print(pattern_list)
        return pattern_list

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------
if __name__ == "__main__":
    s1 = Setter(1,2)
    s1.setPattern(4,3,1)