#!/usr/bin/python

import smbus, time

##  Running this program will move the servo to neutral, pause for two seconds,
##  move it to one extreme, pause for two seconds, then move to the other
##  extreme and exit the program. PWM signal runs at 200 Hz.

bus = smbus.SMBus(1)  # the chip is on bus 1 of the available I2C buses
addr = 0x40           # I2C address of the PWM chip.
##bus.write_byte_data(addr, 0, 0x20)     # enable word writes
##bus.write_byte_data(addr, 0xfe, 0x1e)  # configure the chip for multi-byte write
##bus.write_word_data(addr, 0x06, 0)     # chl 0 start time = 0us
bus.write_byte_data(addr, 0, 0x20) # enables word writes
time.sleep(.25)
bus.write_word_data(addr, 0x06, 0)     # chl 0 start time = 0us

bus.write_word_data(addr, 0x08, 1250)  # chl 0 end time = 1.5ms

## The 1.5ms end time is equal to 1.2us per count. This represents the neutral
##  position of the servo, midway between both extremes. Each degree of
##  deviation from neutral requires that number (1250) to be changed by 4.6.
##  Thus, the 90 degree offset from neutral requires that 414 counts (90*4.6)
##  be added or subtracted from 1250.

## Just for fun, we'll swing the servo to one side and then the other. Note that
##  from now on we only need perform the second write, as the first register we
##  wrote to can remain at zero.

time.sleep(2)   # pause at neutral for two seconds
bus.write_word_data(addr, 0x08, 900)  # chl 0 end time = 1.0ms
time.sleep(2)
bus.write_word_data(addr, 0x08, 1664)  # chl 0 end time = 2.0ms
