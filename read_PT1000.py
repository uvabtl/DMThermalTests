#! /usr/bin/python

import serial
import time
import logging
import sys

# Keithley2231A module would send information to serial port about its function, which wrote it to the data file. This prevents that from happening
def addLoggingLevel(levelName, levelNum, methodName=None):
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        raise AttributeError("{} already defined in logging module".format(levelName))
    if hasattr(logging, methodName):
        raise AttributeError("{} already defined in logging module".format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError("{} already defined in logger class".format(methodName))

    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)

addLoggingLevel("DATA", logging.WARNING - 5)

sys.path.append("/home/uvabtl/Lab5015Utils/")
from Lab5015_utils import Keithley2231A

from optparse import OptionParser       # Allows the user to specify specific command-line argument options
parser = OptionParser()
parser.add_option("-d", "--dev")        # "--dev" lets the user denote a serial port to be given as a command-line argument
parser.add_option("-l", "--log")        # "--log" lets the user denote a data file to be given as a command-line argument
(options, args) = parser.parse_args()   

mykey = Keithley2231A()
mykey_state = 0

logging.basicConfig(format = "%(asctime)s %(message)s", datefmt = "%Y-%m-%d %H:%M:%S", filename = options.log, level = logging.DATA)

port = options.dev

try:
    ser = serial.Serial(port, 115200)
    ser.timeout = 5
except serial.serialutil.SerialException:   # Can't connect to port
    logging.warning("not possible to establish connection with " + str(port))
    self.ser = None
else:
    print("Starting connection with " + str(port))

command = "1"

while True:
    x = ser.write(("1\r\n").encode())
    out = ""                                          # Empty string
    time.sleep(1)                                     # Let's wait one second before reading output (let's give device time to answer)              
    line = ser.readline()                             # Read a byte string
    if line:
        string = line.decode()                        # Convert the byte string to a unicode string
        string = string[:-1]                          # Remove the newline character
        out += string
        out += " " + str(mykey.meas_V()) + " " + str(mykey.meas_I()) + " " + str(mykey.meas_P())
    if out != "":
        logging.data(out.rstrip().lstrip(" "))
    
ser.close()
