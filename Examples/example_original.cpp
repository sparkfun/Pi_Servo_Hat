#include <unistd.h> // required for I2C device access and usleep()
#include <fcntl.h>  // required for I2C device configuration
#include <sys/ioctl.h> // required for I2C device usage
#include <linux/i2c-dev.h> // required for constant definitions
#include <stdio.h>  // required for printf statements

int main(void)
{
  char *filename = (char*)"/dev/i2c-1"; // Define the filename
  int file_i2c = open(filename, O_RDWR); // open file for R/W

  if (file_i2c < 0)
  {
    printf("Failed to open file!");
    return -1;
  }

  int addr = 0x40;    // PCA9685 address
  ioctl(file_i2c, I2C_SLAVE, addr); // Set the I2C address for upcoming
                                    //  transactions

  char buffer[5];   // Create a buffer for transferring data to the I2C device

  // First we need to enable the chip. We do this by writing 0x20 to register
  //  0. buffer[0] is always the register address, and subsequent bytes are
  //  written out in order.
  buffer[0] = 0;    // target register
  buffer[1] = 0x20; // desired value
  int length = 2;       // number of bytes, including address
  write(file_i2c, buffer, length); // initiate write

  // Enable multi-byte writing.

  buffer[0] = 0xfe;  
  buffer[1] = 0x1e;
  write(file_i2c, buffer, length);

  // Write the start time out to the chip. This is the time when the chip will
  //  generate a high output.

  buffer[0] = 0x06;  // "start time" reg for channel 0
  buffer[1] = 0;     // We want the pulse to start at time t=0
  buffer[2] = 0;
  length = 3;        // 3 bytes total written
  write(file_i2c, buffer, length); // initiate the write

  // Write the stop time out to the chip. This is the time when the chip will
  //  generate a low output. The value is in units of 1.2us. 1.5ms corresponds
  //  to "neutral" position. This is where the value 1250 below comes
  //  from.

  buffer[0] = 0x08;   // "stop time" reg for channel 0
  buffer[1] = 1250 & 0xff; // The "low" byte comes first...
  buffer[2] = (1250>>8) & 0xff; // followed by the high byte.
  write(file_i2c, buffer, length); // Initiate the write.

  usleep(2000000); // sleep for 2s.

  // Write stop time again. Don't need to write start time again because we
  //  start time can always be left as zero. 836 corresponds to 1ms time,
  //  which is 90 degrees offset from neutral.
 
  buffer[0] = 0x08;   // "stop time" reg for channel 0
  buffer[1] = 836 & 0xff; // The "low" byte comes first...
  buffer[2] = (836>>8) & 0xff; // followed by the high byte.
  write(file_i2c, buffer, length); // Initiate the write.

  usleep(2000000);

  // Write stop time again. 1664 is 2ms, or 90 degrees offset from neutral in
  //  the opposite direction.
  buffer[0] = 0x08;   // "stop time" reg for channel 0
  buffer[1] = 1664 & 0xff; // The "low" byte comes first...
  buffer[2] = (1664>>8) & 0xff; // followed by the high byte.
  write(file_i2c, buffer, length); // Initiate the write.

  return 0;
}

