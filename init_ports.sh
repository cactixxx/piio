#!/bin/bash

/usr/sbin/i2cset -y 1 0x20 0x00 0x00	#Set ports 1-8 to outputs
/usr/sbin/i2cset -y 1 0x20 0x01 0xE0    #Set ports 9-13 to outputs and 14,15,16 to inputs (1110 0000)
/tools/piio/piio_write.py -a 0x20 -f 0	#Switch all ports off
echo "Ports Initialised"
