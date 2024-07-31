#! /usr/bin/python3

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from time import sleep, strftime, time
from datetime import datetime
import sys

# Interactive mode; used for updating plots
plt.ion()

mytime = []     # Denotes the time stamp of the collected data
mysecs = []     # Denotes the time in between measurements
mytemp1 = []    # Denotes the temperature from the 1st MAX31865 amplifier board (measurement "outside"; from left)     
mytemp2 = []    # Denotes the temperature from the 2nd MAX31865 amplifier board (measurement "outside"; from right)
mytemp3 = []    # Denotes the temperature from the 3rd MAX31865 amplifier board (measurement "inside"; from port 1 on six-pin cable; RTD 1)
mytemp4 = []    # Denotes the temperature from the 4th MAX31865 amplifier board (measurement "inside"; from port 2 on six-pin cable; RTD 2)
mytemp5 = []    # Denotes the temperature from the 5th MAX31865 amplifier board (measurement "inside"; from port 3 on six-pin cable; RTD 3)
mytemp6 = []    # Denotes the temperature from the 6th MAX31865 amplifier board (measurement "inside"; from port 4 on six-pin cable; RTD 4)
mytemp33 = []   # Denotes temperature change between RTD 1 and outside ambient temperature
mytemp44 = []   # Denotes temperature change between RTD 2 and outside ambient temperature
mytemp55 = []   # Denotes temperature change between RTD 3 and outside ambient temperature
mytemp66 = []   # Denotes temperature change between RTD 4 and outside ambient temperature

# The file from which we're reading data
file = sys.argv[1]

# Plot the data
def graph():

    # Clears the current figure
    plt.clf()
    
    # Creates the first of two subplots to be placed on top
    plt.subplot(211)
    
    plt.plot(mysecs, mytemp1, color = "black", linestyle = "dashed", label = "Copper Left")    # Temperature outside DM on top as a function of time  
    plt.plot(mysecs, mytemp2, color = "black", linestyle = "dotted", label = "Copper Right")   # Temperature outside DM on bottom as a function of time
    plt.plot(mysecs, mytemp3, label = "Bottom Left", color = "blue")                           # Temperature from RTD 1 as a function of time
    plt.plot(mysecs, mytemp4, label = "Bottom Right", color = "green")                         # Temperature from RTD 2 as a function of time
    plt.plot(mysecs, mytemp5, label = "Top Left", color = "red")                               # Temperature from RTD 3 as a function of time
    plt.plot(mysecs, mytemp6, label = "Top Right", color = "gold")                             # Temperature from RTD 4 as a function of time
    plt.xlabel("Time Elapsed [min.]")                                                          # Time in minutes
    plt.ylabel("Temperature [\u00B0C]")                                                        # "\u00B0" is the degree symbol in Unicode
    plt.grid()                                                                                 # Creates a grid
    plt.ylim([10.0, 50.0])                                                                     # Range of temperatures
    plt.legend(loc = "upper right", prop = {"size": 8}, shadow = True, edgecolor = "black")    # Legend
    
    # Creates the second of two subplots to be placed on bottom
    plt.subplot(212)

    plt.plot(mysecs, mytemp33, label = "Bottom Left", color = "blue")     # Temperature difference between RTD 1 and outside temperature closest to RTD 1 as a function of power
    plt.plot(mysecs, mytemp44, label = "Bottom Right", color = "green")   # Temperature difference between RTD 2 and outside temperature closest to RTD 2 as a function of power
    plt.plot(mysecs, mytemp55, label = "Top Left", color = "red")         # Temperature difference between RTD 3 and outside temperature closest to RTD 3 as a function of power
    plt.plot(mysecs, mytemp66, label = "Top Right", color = "gold")       # Temperature difference between RTD 4 and outside temperature closest to RTD 4 as a function of power
    plt.xlabel("Time Elapsed [min.]")                                     # Time in minutes
    plt.ylabel("\u0394T [\u00B0C]")                                       # "\u0394" is the Greek letter delta in Unicode          
    plt.grid()
    plt.ylim([-30.0, 3.0])                                                # Limits are different since these are temperature changes
    plt.text(0.05, -24, "Max \u0394T: {0}\u00B0C".format(round(min([ele for ele in mytemp33]), 2)), fontsize = 9, color = "blue")      # Label for maximum temperature difference from RTD 1
    plt.text(0.05, -25.5, "Max \u0394T: {0}\u00B0C".format(round(min([ele for ele in mytemp44]), 2)), fontsize = 9, color = "green")   # Label for maximum temperature difference from RTD 2
    plt.text(0.05, -27, "Max \u0394T: {0}\u00B0C".format(round(min([ele for ele in mytemp55]), 2)), fontsize = 9, color = "red")       # Label for maximum temperature difference from RTD 3
    plt.text(0.05, -28.5, "Max \u0394T: {0}\u00B0C".format(round(min([ele for ele in mytemp66]), 2)), fontsize = 9, color = "gold")    # Label for maximum temperature difference from RTD 4
    plt.legend(loc = "upper right", prop = {"size": 8}, shadow = True, edgecolor = "black")

    # Prevent the axis labels and subplot titles from overlapping
    plt.tight_layout()
    
    # Show the plot
    plt.show()

# Initially plot all data contained in the data file
with open(str(file), "r") as fin:
    for line in fin.readlines():

        readings = line.strip().split()   # Create a list of all the data in the file
        if len(readings) != 8:            # Don't include any lines that contain faults, errors, etc.
            continue;                     # Could not tell you why there's a semicolon here
    
        mytime.append(datetime.strptime(readings[0] + " " + readings[1], "%Y-%m-%d %H:%M:%S"))   # Add timestamps
        if len(mysecs) == 0:                                                                     # If there's nothing in mysecs...
            mysecs.append(0)                                                                     # "0" denotes the start of the data run
        else:                                                                                    # If there's something in mysecs...
            mysecs.append((mytime[-1] - mytime[0]).total_seconds() / 60.0)                       # Find the total number of seconds between the start of the run and the last data point collected, then convert to minutes

        # Adding data to respective lists
        mytemp1.append(float(readings[2]))
        mytemp2.append(float(readings[3]))
        mytemp3.append(float(readings[4]))
        mytemp4.append(float(readings[5]))
        mytemp5.append(float(readings[6]))
        mytemp6.append(float(readings[7]))

        # Subtract corresponding outside temperatures from each RTD reading and add to respective lists
        mytemp33.append(mytemp3[-1] - mytemp1[-1])
        mytemp44.append(mytemp4[-1] - mytemp2[-1])
        mytemp55.append(mytemp5[-1] - mytemp1[-1])
        mytemp66.append(mytemp6[-1] - mytemp2[-1])

        # Print the time and the temperature readings to the screen
        print(str(readings[1]) + " " + str(readings[2]) + " " + str(readings[3]) + " " + str(readings[4]) + " " + str(readings[5]) + " " + str(readings[6]) + " " + str(readings[7]))

# Add data as it comes (much the same as before)
while True:
    try:
        with open(str(file), "r") as fin:
            for line in fin.readlines()[-1:]:
                readings = line.strip().split()
                if len(readings) != 8:
                    continue;
                mytime.append(datetime.strptime(readings[0] + " " + readings[1], "%Y-%m-%d %H:%M:%S"))
                mysecs.append((mytime[-1] - mytime[0]).total_seconds() / 60.0)
                mytemp1.append(float(readings[2]))
                mytemp2.append(float(readings[3]))
                mytemp3.append(float(readings[4]))
                mytemp4.append(float(readings[5]))
                mytemp5.append(float(readings[6]))
                mytemp6.append(float(readings[7]))
                mytemp33.append(mytemp3[-1] - mytemp1[-1])
                mytemp44.append(mytemp4[-1] - mytemp2[-1])
                mytemp55.append(mytemp5[-1] - mytemp1[-1])
                mytemp66.append(mytemp6[-1] - mytemp2[-1])
                print(str(readings[1]) + " " + str(readings[2]) + " " + str(readings[3]) + " " + str(readings[4]) + " " + str(readings[5]) + " " + str(readings[6]) + " " + str(readings[7]))
                graph()
                plt.pause(3)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt")
        sys.exit(1)
