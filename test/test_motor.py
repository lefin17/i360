#!/usr/bin/python3

import sys
import os 

sys.path.append(os.path.abspath("/home/lefin/work/i360/classes"))
from motor import * 

motor = Motor()

print (motor.speed)
