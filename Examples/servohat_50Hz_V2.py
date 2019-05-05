import smbus, time
bus = smbus.SMBus(1)
addr = 0x40

## Running this program will move the servo to 0, 45, and 90 degrees with 5 second pauses in between with a 50 Hz PWM signal.

bus.write_byte_data(addr, 0, 0x20) # enable the chip
time.sleep(.25)
bus.write_byte_data(addr, 0, 0x10) # enable Prescale change as noted in the datasheet
time.sleep(.25) # delay for reset
bus.write_byte_data(addr, 0xfe, 0x79) #changes the Prescale register value for 50 Hz, using the equation in the datasheet.
bus.write_byte_data(addr, 0, 0x20) # enables the chip

time.sleep(.25)
bus.write_word_data(addr, 0x06, 0) # chl 0 start time = 0us

def servo_example():
    time.sleep(1)
    bus.write_word_data(addr, 0x08, 209) # chl 0 end time = 1.0ms (0 degrees)
    time.sleep(1)
    bus.write_word_data(addr, 0x08, 312) # chl 0 end time = 1.5ms (45 degrees)
    time.sleep(1)
    bus.write_word_data(addr, 0x08, 416) # chl 0 end time = 2.0ms (90 degrees)

def set_servo(channel, position):
    #debug variables passed to this function
    print("channel: " + str (channel) + "\t" + "position: " + str (position))
    #time.sleep(1)

    #shift address to correct channel start and stop addresses
    start_addr = 0x06 + (4*channel)
    stop_addr = 0x08 + (4*channel)
    #print("start_addr: " + str (start_addr) + "\t" + "stop_addr: " + str (stop_addr))

    #convert position (degrees 0-90) to a fraction of the 5ms period, which can be 0-4095
    degree_90_val = 416
    degree_0_val = 209
    full_swing_difference = (degree_90_val - degree_0_val)

    # position comes in as 0 - 90, and this is a fraction of the full_swing_difference
    #
    degree_offset_val = round(full_swing_difference * (position / 90 ))
    
    position_val = (degree_0_val + degree_offset_val)
    
    #print("full_swing_difference: " + str (full_swing_difference) + "\t" + "degree_offset_val: " + str (degree_offset_val) + "\t" + "position_val: " + str (position_val))

    #write start and stop to channel
    bus.write_word_data(addr, start_addr, 0) # channel start time = 0us for all
    bus.write_word_data(addr, stop_addr, position_val) # channel stop time is a special position val calculated above

    
    
               

while 1:
    for x in range(16):
        for y in range(3):
            set_servo(x, (45*y)) # set 0, then 45, then 90 as y increments
            time.sleep(1)
        time.sleep(5) # allow time to move to next channel during testing  
    #servo_example


