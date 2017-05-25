#!/usr/bin/python

import argparse
import smbus
import sys
#import time

__author__ = 'Ernst du Plooy'
__version_info__ = ('2016','03','21')
__version__ = '-'.join(__version_info__)
__example__ = """Examples:
%(prog)s -a 0x20			Output values of all pins for board with address 0x20
					Execute sudo i2cdetect -y 1 to get the board address.
%(prog)s -a 0x20 -p 2,10,7		Output values of pins 2,10,7 (in that order)
%(prog)s -a 0x20 -p 1,5,9 -v	Print values of pins 1,5,9 in verbose mode
%(prog)s -a 0x20 -p 2,2,2 -v	Print values of pin 2 three times in verbose mode

"""

def get_args():
    parser = argparse.ArgumentParser(
        description='Read and print values from the Zee PIIO board',
	epilog=__example__,formatter_class=argparse.RawDescriptionHelpFormatter)

    requiredNamed = parser.add_argument_group('required arguments')
    requiredNamed.add_argument(
        '-a', '--address', type=str, help='Board Address', required=True)
    parser.add_argument(
        '-p', '--pin', type=str, help='Pin number(s) [1..16] to read.', nargs='+')
    parser.add_argument(
        '-v', '--verbose', action="store_true", help="Show verbose results", required=False, default=None)
    parser.add_argument('--version', action='version', version="%(prog)s ("+__version__+")\nAuthor: "+__author__+"")
    args = parser.parse_args()
    address = args.address
    verbose = args.verbose
    try:
	    pin = args.pin[0].split(",")
    except:
	    pin = None
    return address, pin, verbose

#########################################################################

address, pin, verbose = get_args()

bus = smbus.SMBus(1)    

DEVICE_ADDRESS = int(address, 16)
IODIRA = 0x00
IODIRB = 0x01
GPIOA = 0x12
GPIOB = 0x13
OLATA = 0x14
OLATB = 0x15

gpa = bus.read_byte_data(DEVICE_ADDRESS, GPIOA)
gpb = bus.read_byte_data(DEVICE_ADDRESS, GPIOB)
gp = bin(gpb)[2:].zfill(8) + bin(gpa)[2:].zfill(8)
gp_r = gp[::-1]		#Swap array around
latcha = bus.read_byte_data(DEVICE_ADDRESS, OLATA)
latchb = bus.read_byte_data(DEVICE_ADDRESS, OLATB)
lp = bin(latchb)[2:].zfill(8) + bin(latcha)[2:].zfill(8)

if verbose:
	print "\nBoard address:\t[ %s ]" % address
	print "Port state:\t[ %s ]" % gp
	print "Latch state:\t[ %s ]\n" % lp

if pin is not None:
	for p in pin:
		if int(p) < 1 or int(p) > 16:
			sys.exit("Port value must be between 1 and 16")
		if verbose:
			print "Pin %d:\t%s" % (int(p), gp_r[int(p)-1])
		else:
			print gp_r[int(p)-1],
	print
else:
	if verbose:
		for x in range(0, 16):
			print "Pin %d:\t%s" % (int(x+1), gp_r[int(x)])
		print
	else:
		result = ''
		for ch in gp:
			result = result + ch + ' '
		print(result[:-1])
