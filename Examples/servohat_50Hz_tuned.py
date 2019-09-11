import smbus, time
bus = smbus.SMBus(1)
addr = 0x40

## Running this program will move the servo to 0, 45, and 90 degrees with 5 second pauses in between with a 50 Hz PWM signal.

bus.write_byte_data(addr, 0, 0x20) # enable word writes
time.sleep(.25)
bus.write_byte_data(addr, 0, 0x10) # enable Prescale change as noted in the datasheet
time.sleep(.25) # delay for reset
bus.write_byte_data(addr, 0xfe, 0x88) #changes the Prescale register value for 50 Hz, using the equation in the datasheet (I later adjusted the value to fine tune the signal with an oscilloscope. The original value was 0x79.)
time.sleep(.25)
bus.write_byte_data(addr, 0, 0x20) # enables word writes

time.sleep(.25)
bus.write_word_data(addr, 0x06, 0) # chl 0 start time = 0us
               
time.sleep(.25)
bus.write_word_data(addr, 0x08, 250) # chl 0 end time = 1.0ms (0 degrees) (I later adjusted the value to fine tune it to the servo I was testing with. The original value was 209, which matched perfectly to a 1ms signal an oscilloscope with the 0x88 prescaler value.)
time.sleep(5)
bus.write_word_data(addr, 0x08, 350) # chl 0 end time = 1.5ms (45 degrees) (I later adjusted the value to fine tune it to the servo I was testing with. The original value was 312, which matched perfectly to a 1.5ms signal an oscilloscope with the 0x88 prescaler value.)
time.sleep(5)
bus.write_word_data(addr, 0x08, 440) # chl 0 end time = 2.0ms (90 degrees) (I later adjusted the value to fine tune it to the servo I was testing with. The original value was 416, which matched perfectly to a 2ms signal an oscilloscope with the 0x88 prescaler value.)
