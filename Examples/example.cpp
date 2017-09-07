#include <unistd.h> // required for I2C device access
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
  buffer[0] = 0;    // target register
  buffer[1] = 0x20; // desired value
  length = 2;       // number of bytes, including address
  write(file_i2c, buffer, length); // initiate write

  buffer[0] = 0xfe;
  buffer[1] = 0x1e;
  write(file_i2c, buffer, length);

  buffer[0] = 0x06;  // "start time" reg for channel 0
  buffer[1] = 0;     // We want the pulse to start at time t=0
  buffer[2] = 0;
  length = 3;        // 3 bytes total written
  write(file_i2c, buffer, length); // initiate the write

  buffer[0] = 0x08;   // "stop time" reg for channel 0
  buffer[1] = 1250 & 0xff; // The "low" byte comes first...
  buffer[2] = (1250>>8) & 0xff; // followed by the high byte.
  write(file_i2c, buffer, length); // Initiate the write.
  return 0;
}

