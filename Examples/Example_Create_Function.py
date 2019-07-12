import smbus, time
bus = smbus.SMBus(1)
addr = 0x40

def servo_Init(channel):
     # Mapping Channel Register
     channel_0_start = 0x06
     channel_reg = 4*channel + channel_0_start
     
     # Write to Channel Register
     bus.write_word_data(addr, channel_reg, 0) 


def servo_Pos(channel, deg_range, deg_position):
     # Mapping Channel Register
     channel_0_end = 0x08
     channel_reg = 4*channel + channel_0_end
     
     # Mapping Sevo Arm Position
     #   209 = 0 deg
     #   312 = 45 deg
     #   416 = 90 deg
     deg_0 = 209
     deg_max = 416
     pos_end_byte = lambda x: (deg_max-deg_0)/deg_range*x + deg_0
     
     # Write to Channel Register
     bus.write_word_data(addr, channel_reg, round(pos_end_byte(deg_position)))

## Running this program will move the servo to 0, 45, and 90 degrees with 5 second pauses in between with a 50 Hz PWM signal.

# Configure 50Hz PWM Output
bus.write_byte_data(addr, 0, 0x20) # enable the chip
time.sleep(.25)
bus.write_byte_data(addr, 0, 0x10) # enable Prescale change as noted in the datasheet
time.sleep(.25) # delay for reset
bus.write_byte_data(addr, 0xfe, 0x79) #changes the Prescale register value for 50 Hz, using the equation in the datasheet.
bus.write_byte_data(addr, 0, 0x20) # enables the chip

# Initialize Channel (sets start time for channel)
servo_Init(3)

# Run Loop
while True:
     time.sleep(.5)
     servo_Pos(3, 90, 0) # chl 3 end time = 1.0ms (0 degrees)
     time.sleep(.5)
     servo_Pos(3, 90, 45) # chl 3 end time = 1.5ms (45 degrees)
     time.sleep(.5)
     servo_Pos(3, 90, 0) # chl 3 end time = 1.0ms (0 degrees)
     time.sleep(.5)
     servo_Pos(3, 90, 90) # chl 3 end time = 2.0ms (90 degrees)

