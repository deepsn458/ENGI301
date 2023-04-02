# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Basic example of turning on LEDs and handling Keypad
# button activity.

# This example uses only one Trellis board, so all loops assume
# a maximum of 16 LEDs (0-15). For use with multiple Trellis boards,
# see the documentation.

import time
import busio
import board
from adafruit_trellis import Trellis

# Create the I2C interface
i2c = busio.I2C(board.SCL_2, board.SDA_2)

# Create a Trellis object
trellis_1 = Trellis(i2c)
trellis_2 = Trellis(i2c,[0x71])  # 0x70 when no I2C address is supplied

# 'auto_show' defaults to 'True', so anytime LED states change,
# the changes are automatically sent to the Trellis board. If you
# set 'auto_show' to 'False', you will have to call the 'show()'
# method afterwards to send updates to the Trellis board.

# Turn on every LED
print("Turning all LEDs on...")
trellis_1.led.fill(True)
trellis_2.led.fill(False)
time.sleep(2)

# Turn off every LED
print("Turning all LEDs off...")
trellis_1.led.fill(False)
trellis_2.led.fill(True)
time.sleep(2)

# Turn on every LED, one at a time
print("Turning on each LED, one at a time...")
for i in range(16):
    trellis_1.led[i] = True
    trellis_2.led[i] = False
    time.sleep(0.1)

# Turn off every LED, one at a time
print("Turning off each LED, one at a time...")
for i in range(15, 0, -1):
    trellis_2.led[i] = True
    trellis_1.led[i] = False
    time.sleep(0.1)

# Now start reading button activity
# - When a button is depressed (just_pressed),
#   the LED for that button will turn on.
# - When the button is relased (released),
#   the LED will turn off.
# - Any button that is still depressed (pressed_buttons),
#   the LED will remain on.
print("Starting button sensory loop...")
pressed_buttons = set()



#--------------------------------------------------
# test the press reading
# ----------------------------------------------------
while True:
    # Make sure to take a break during each trellis.read_buttons
    # cycle.
    time.sleep(0.1)

    just_pressed, released = trellis_1.read_buttons()
    print(just_pressed)
    for b in just_pressed:
        print("pressed:", b)
        trellis_2.led[b] = True
    pressed_buttons.update(just_pressed)
    for b in released:
        print("released:", b)
        trellis_2.led[b] = False
    pressed_buttons.difference_update(released)
    for b in pressed_buttons:
        print("still pressed:", b)
        trellis_2.led[b] = True