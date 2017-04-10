#!/bin/bash
#Version 0.1

VERBOSE=true		#Change this to false if no screen output is required

if [ -z "$1" ]; then
  echo "You must supply the address of the Zee PIIO board"
  echo " "
  echo "Usage: piio_init.sh address [port] [value]"
  echo "Examples: 	piio_init.sh 0x20		- This will set all pins as outputs"
  echo "		piio_init.sh 0x20 A		- This will set all pins on PortA (pins 1-8) as outputs"
  echo "		piio_init.sh 0x20 B		- This will set PortB (pins 9-16) as  outputs"
  echo "		piio_init.sh 0x20 A 0xFF	- This will set all pins on PortA (pins 1-8) as inputs"
  echo "		piio_init.sh 0x20 A 0x00	- This will set all pins on PortA (pins 1-8) as outputs"
  echo "		piio_init.sh 0x20 A 0xF5	- This will set pins 1,3,5,6,7,8 as inputs and 2,4 as outputs"
  echo " "
  echo "Please read the Zee PIIO quick start guide for more information"
  exit
fi

if ! [[ $1 =~ ^(0x20|0x21|0x22|0x23|0x24|0x25|0x26|0x27)$ ]]; then 
    echo "ERROR: An invalid Zee PIIO board address was given.  The address must be between 0x20 to 0x27."
    exit
fi

if [ -z "$2" ]; then
  if [ "$VERBOSE" = true ]; then
    echo "Setting all ports (pins 1-16) as outputs"
  fi
  /usr/sbin/i2cset -y 1 $1 0x00 0x00	#Set ports 1-8 as outputs
  /usr/sbin/i2cset -y 1 $1 0x01 0x00  #Set ports 9-16 as outputs
  exit
fi

if [ -z "$3" ]; then
  VALUE=0x00
else
  VALUE=$3
fi

if [[ $2 =~ ^(A|a|B|b)$ ]]; then 
  if [[ $2 =~ ^(A|a)$ ]]; then
    if [ "$VERBOSE" = true ]; then
      echo "Setting Port A (pins 1-8) as $VALUE"
      /usr/sbin/i2cset -y 1 0x20 0x00 $VALUE
      if [ "$?" == 1 ]; then
        echo " "
        echo "ERROR: An invalid value was given.  The value must be between 0x00 and 0xFF."
        exit;
      fi
    fi
  fi
  if [[ $2 =~ ^(B|b)$ ]]; then
    if [ "$VERBOSE" = true ]; then
      echo "Setting Port B (pins 9-16) as $VALUE"
      /usr/sbin/i2cset -y 1 0x20 0x01 $VALUE
      if [ "$?" == 1 ]; then
        echo " "
        echo "ERROR: An invalid value was given.  The value must be between 0x00 and 0xFF."
        exit;
      fi
    fi
  fi
else
  echo "Invalid Port. The Port must be either A or B"
fi

