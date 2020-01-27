#!/usr/bin/python3

import sys
import os 

sys.path.append(os.path.abspath("/home/lefin/work/i360/classes"))
from motor import * 

motor = Motor(20, 50, "CCW")

print (motor.speed)

# a = motor.serial_ports()

motor.connect()

