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
The guesser module provides the methods that will manipulate the hardware for the guesser

APIs:
  - Guesser(led, trellis)
    - led is an instance of the led class
    - trellis is the instance of the trellis class

    - getLed()
        - returns the guesser's led object
    - getTrellis()
        - returns the guesser's trellis object
    - updateScore()
        - updates the guesser's score
    - getScore()
        - returns the guesser's score
"""

# ------------------------------------------------------------------------
# Main Tasks
# ------------------------------------------------------------------------
class Guesser():
    trellis = None
    led = None
    score = 0
    
    def __init__(self, trellis, led):
        self.trellis = trellis
        self.led = led
    #end def
    
    def getLED(self):
        """Returns the guesser's led object"""
        return self.led
    
    #end def
    
    def getTrellis(self):
        """Returns the guesser's trellis object"""
        return self.trellis
    #end def
    
    def updateScore(self):
        """ Updates the guesser's score"""
        self.score += 1
        self.led.update(self.score)
    #end def
    
    def getScore(self):
        """Returns the guesser's score"""
        return self.score
    #end def
#end class