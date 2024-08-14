#! /usr/bin/python3

import os
import sys
import time
import subprocess
from subprocess import Popen, PIPE 
from optparse import OptionParser
from datetime import datetime 

sys.path.append("/home/uvabtl/Lab5015Utils/")
from Lab5015_utils import Keithley2231A

parser = OptionParser()
parser.add_option("-r", "--run")
(options, args) = parser.parse_args()

mykey = Keithley2231A()
mykey_state = 0

proc = Popen(["python3", "/home/uvabtl/Detector_Module_QAQC/DMThermalTests/read_PT1000.py", "--dev", "/dev/ttyACM0", "--log", "run%04d.log"%int(options.run)])
pid = proc.pid
print(pid)

timestamp_init = datetime.now() 

time.sleep(3)

while True:
    try:
        os.system("tail -n 1 run%04d.log"%int(options.run)) 
        time.sleep(2)
        
        timestamp_curr = datetime.now()
        time_elapsed = float((timestamp_curr - timestamp_init).total_seconds())
        if ((time_elapsed > 30.0) and (time_elapsed < 240.0) and (mykey_state == 0)):
            mykey.set_V(20)
            mykey.set_state(1)
            mykey_state = 1
        
        if (time_elapsed > 240.0):
            mykey.set_V(0)
            mykey.set_state(0)
            mykey_state = 0
        
        if (time_elapsed > 300.0):
            break
    
    except KeyboardInterrupt:
        break

print("killing process %d"%pid)
os.system("kill -9 %d"%pid) 

mykey.set_V(0)
mykey.set_state(0)
