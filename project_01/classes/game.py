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
        - setPatternSize()
            - Sets the number of presses for each pattern
            
        - checkPress(location, pattern_list, press_counter)
            - Checks if the guesser pressed the correct key
            - location is the key pressed
            - pattern_list represents the pattern set by the setter
            - press_counter is the current step in the pattern
        
        - checkWinner(p1_score, p2_score)
            - checks if any player/cpu has reached 10 points
            - p1_score is the score of player 1
            - p2_score is the score of player 2 or the cpu
        
        - guessPattern(guesser, pattern_size, pattern_list)
            - checks if the guesser guessed the whole pattern correctly
            - guesser is an instance of the Guesser class
            - pattern_list is the pattern set by the setter
            - pattern_size is the length of pattern_list
        
        - OnePlayer(Game)
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