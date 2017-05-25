#include <stdint.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/types.h>
#include <linux/i2c-dev.h>
#include <stdlib.h>

//#define I2C_ADDR 0x20				// Device adress

#define MCP23017_IODIRA 0                       // IODIRA (see data sheet)
#define MCP23017_IODIRB 1			// IODIRB (see data sheet)
#define MCP23017_GPPUA 0x0C                     // GPPUA (see data sheet)
#define MCP23017_GPIOA 0x012                    // GPIOA (see data sheet)
#define MCP23017_GPIOB 0x013                    // GPIOB (see data sheet)

static const char *device = "/dev/i2c-1";	// I2C bus

static void exit_on_error (const char *s)	// Exit and print error code
{ 	perror(s);
  	abort();
} 

int main(int argc, char *argv[])
{
	int fd;
	uint8_t buffer[2];
	uint8_t I2C_ADDR;
	if (argc != 2)
        {
          printf ("Usage:\n  read_mcp23017 ADDRESS\nExample: read_mcp23017 0x20\n\n");
	  exit(-1);
	}
        //I2C_ADDR = 0x20;
        I2C_ADDR = strtol(argv[1], NULL, 16);

       	// Open I2C device
       	if ((fd = open(device, O_RDWR)) < 0) exit_on_error ("Can't open I2C device");

	// Set I2C slave address
	if (ioctl(fd, I2C_SLAVE,I2C_ADDR) < 0) exit_on_error ("Can't talk to slave");
        
        // Read from PortB                                                
        buffer[0] = MCP23017_GPIOB;
        if (write(fd,buffer,1) != 1) exit_on_error ("Failed to write to the i2c bus [5]");                                                            
        if (read(fd,buffer,1) != 1 ) exit_on_error ("Failed to read from the i2c bus");  
        printf("%02X", buffer[0]);      
        // Read from PortA                                                
        buffer[0] = MCP23017_GPIOA;
        if (write(fd,buffer,1) != 1) exit_on_error ("Failed to write to the i2c bus [5]");                                                            
        if (read(fd,buffer,1) != 1 ) exit_on_error ("Failed to read from the i2c bus");  
        printf("%02X", buffer[0]);      
        
        close(fd);

	return (0);
}
