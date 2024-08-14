#! /usr/bin/python

import serial
import time
import logging

from optparse import OptionParser       # Allows the user to specify specific command-line argument options
parser = OptionParser()
parser.add_option("-d", "--dev")        # "--dev" lets the user denote a serial port to be given as a command-line argument
parser.add_option("-l", "--log")        # "--log" lets the user denote a data file to be given as a command-line argument
(options, args) = parser.parse_args()   

logging.basicConfig(format = "%(asctime)s %(message)s", datefmt = "%Y-%m-%d %H:%M:%S", filename = options.log, level = logging.DEBUG)

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
    #time.sleep(0.5)
    #data = ser.readline()[:-2]                        # The last bit gets rid of the new-line characters
    #if data:
    #	print(data)
    x = ser.write(("1\r\n").encode())
    out = ""                                          # Empty string
    time.sleep(1)                                     # Let's wait one second before reading output (let's give device time to answer)              
    line = ser.readline()                             # Read a byte string
    if line:
        string = line.decode()                        # Convert the byte string to a unicode string
        string = string[:-1]                          # Remove the newline character 
        out += string
    if out != "":
        logging.info(out.rstrip().lstrip(" "))
    
ser.close()
