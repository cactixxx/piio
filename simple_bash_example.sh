#!/bin/bash

P='/home/pi/piio'

$P/piio_init.sh 0x20 A		#Configure all pins 1-8 as outputs
$P/piio_write.py -a 0x20 -f 0	#Switch all outputs off
while :
do
  $P/piio_write.py -a 0x20 -o 1,3,5 -f 2,4
  sleep 1
  $P/piio_write.py -a 0x20 -o 2,4 -f 1,3,5
  sleep 1
done
