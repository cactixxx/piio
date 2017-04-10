#!/usr/bin/python

import argparse
import smbus
import sys
#import time

__author__ = 'Ernst du Plooy'
__version_info__ = ('2017','05','31')
__version__ = '-'.join(__version_info__)
__example__ = """Examples:
%(prog)s -a 0x20 -o 0			Switch all ports on using board address 0x20.
						Execute sudo i2cdetect -y 1 to get the board address.
%(prog)s -a 0x20 --on 0			Same as above example
%(prog)s -a 0x20 --on=0			Same as above example
%(prog)s -a 0x20 -f 0			Switch all ports off
%(prog)s -a 0x20 -o 0 -f 0			Switch all ports off since --off has a higher prioroty than --on
%(prog)s -a 0x20 -o 1,3,11			Switch on ports 1,3,11 
%(prog)s -a 0x20 -o 1,3,11 -v		Same as above example, but screen output will be in verbose mode
%(prog)s -a 0x20 -f 1,3,11			Switch off ports 1,3,11 
%(prog)s -a 0x20 -o 1,3,11 -f 2,12		Switch ports 1,3,11 on and 2,12 off 
%(prog)s -a 0x20 -o 1,3,11 -f 1,3		Switch on port 11 only (since --off has a higher priority than --on) 
"""

def get_args():
    parser = argparse.ArgumentParser(
        description='Set outputs on the Zee PIIO board',
	epilog=__example__,formatter_class=argparse.RawDescriptionHelpFormatter)

    requiredNamed = parser.add_argument_group('required arguments')
    requiredNamed.add_argument(
        '-a', '--address', type=str, help='Board Address', required=True)
    parser.add_argument(
        '-o', '--on', type=str, help='Pin number(s) [0..16] to switch on. Pin number 0 will switch on all pins.', nargs='+')
    parser.add_argument(
        '-f', '--off', type=str, help='Pin number(s) [0..16] to switch off. Pin number 0 will switch off all pins. --off will have a higher priority than --on', nargs='+')
    parser.add_argument(
        '-v', '--verbose', action="store_true", help="Show result on screen", required=False, default=None)
    parser.add_argument('--version', action='version', version="%(prog)s ("+__version__+")\nAuthor: "+__author__+"")
    args = parser.parse_args()
    address = args.address
    verbose = args.verbose
    try:
	    on = args.on[0].split(",")
    except:
	    on = None
    try:
	    off = args.off[0].split(",")
    except:
	    off = None
    return address, on, off, verbose

#########################################################################

address, on, off, verbose = get_args()

bus = smbus.SMBus(1)    

DEVICE_ADDRESS = int(address, 16)
IODIRA = 0x00
IODIRB = 0x01
OLATA = 0x14
OLATB = 0x15


on_b = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
res_b = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
off_b = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

gpa = bus.read_byte_data(DEVICE_ADDRESS, OLATA)
gpb = bus.read_byte_data(DEVICE_ADDRESS, OLATB)
gp = bin(gpb)[2:].zfill(8) + bin(gpa)[2:].zfill(8)

if on is not None:
	if on[0] == "0":
		on_b = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
	else:
		for p in on:
			if int(p) < 1 or int(p) > 16:
				sys.exit("Port value must be between 1 and 16")
			on_b[int(p)-1] = 1

if off is not None:
	if off[0] == "0":
		off_b = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
	else:
		for p in off:
			if int(p) < 1 or int(p) > 16:
				sys.exit("Port value must be between 1 and 16")
			off_b[int(p)-1] = 1

on_b = list(reversed(on_b))
off_b = list(reversed(off_b))
for x in range(0, 16):
	if off_b[x] == 1:
		res_b[x] = 0
	else:
		res_b[x] = int(on_b[x]) | int(gp[x])

if verbose:
	print "\nBoard address:\t[ %s ]" % address
	print "Current state:\t[ %s ]" % gp
	print "Switch On:\t%s" % on_b
	print "Switch Off:\t%s" % off_b
	print "Result:\t\t%s\n" % res_b

resA = 0
resB = 0
res_b = list(reversed(res_b))
for x in range(0, 16):
	if res_b[x] == 1:
		if x < 8:
			resA = resA + 2**x
		else:
			resB = resB + 2**(x)/256

bus.write_byte_data(DEVICE_ADDRESS, OLATA , resA)
bus.write_byte_data(DEVICE_ADDRESS, OLATB , resB)
