#!/bin/bash
# --------------------------------------------------------------------------
# Pattern Guesser - Configure Pins
# --------------------------------------------------------------------------
# License:   
# Copyright 2023 Deepak Narayan
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this 
# list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors 
# may be used to endorse or promote products derived from this software without 
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# --------------------------------------------------------------------------
# 
# Configure pins for the Pattern Guesser game:
#   - I2C1 for LED Displays
#   - I2C2 for Trellises
#   - GPIO for  Buttons
#   - 
# --------------------------------------------------------------------------

# I2C1
config-pin P2_09 i2c
config-pin P2_11 i2c

#I2C2
config-pin P1_26 i2c
config-pin P1_28 i2c

# Select button
config-pin P2_22 gpio
#Right button
config-pin P2_20 gpio
#Left button
config-pin P2_18 gpio

#RS pin for LCD
config-pin P1_02 gpio
# Enable for LCD
config-pin P1_04 gpio

#data lines 4 to 7 for LCD
config-pin P2_02
config-pin P2_04
config-pin P2_06
config-pin P2_08