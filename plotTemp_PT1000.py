#! /usr/bin/python3

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from time import sleep, strftime, time
from datetime import datetime
import sys

plt.ion()

mytime = []
mysecs = []
mytemp1= []
mytemp2= []
mytemp3= []
mytemp4= []
mytemp5= []
mytemp6= []
mytemp33= []
mytemp44= []
mytemp55= []
mytemp66= []

file=sys.argv[1]


def graph():
    
    plt.clf()
    
    axes = plt.gca()
    plt.subplot(211)
    plt.plot(mysecs,mytemp1,color='black',linestyle='dashed')
    plt.plot(mysecs,mytemp2,color='black',linestyle='dotted')
    plt.plot(mysecs,mytemp3)
    plt.plot(mysecs,mytemp4)
    plt.plot(mysecs,mytemp5)
    plt.plot(mysecs,mytemp6)
    plt.xlabel("time elapsed [min.]")
    plt.ylabel("temperature [C]")
    plt.grid()
    plt.ylim([15.,40.])
    plt.subplot(212)
    plt.plot(mysecs,mytemp33)
    plt.plot(mysecs,mytemp44)
    plt.plot(mysecs,mytemp55)
    plt.plot(mysecs,mytemp66)
    plt.xlabel("time elapsed [min.]")
    plt.ylabel("Delta T [C]")
    plt.grid()
    plt.ylim([-20.,10.])
    plt.show()




with open(str(file), 'r') as fin:
    #for line in fin.readlines() [-200]:
    for line in fin.readlines():
        readings = line.strip().split()
        if len(readings) != 8:
            continue;
        
        mytime.append(datetime.strptime(readings[0]+" "+readings[1], "%Y-%m-%d %H:%M:%S"))
        if len(mysecs) == 0:
            mysecs.append(0)
        else:
            mysecs.append((mytime[-1]-mytime[0]).total_seconds()/60.)        
        mytemp1.append(float(readings[2]))
        mytemp2.append(float(readings[3]))
        mytemp3.append(float(readings[4]))
        mytemp4.append(float(readings[5]))
        mytemp5.append(float(readings[6]))
        mytemp6.append(float(readings[7]))
        mytemp33.append(mytemp3[-1]-0.5*(mytemp1[-1]+mytemp2[-1]))
        mytemp44.append(mytemp4[-1]-0.5*(mytemp1[-1]+mytemp2[-1]))
        mytemp55.append(mytemp5[-1]-0.5*(mytemp1[-1]+mytemp2[-1]))
        mytemp66.append(mytemp6[-1]-0.5*(mytemp1[-1]+mytemp2[-1]))
        print(str(readings[1])+" "+str(readings[2])+" "+str(readings[3])+" "+str(readings[4])+" "+str(readings[5])+" "+str(readings[6])+" "+str(readings[7]))
        

while True:
    with open(str(file), 'r') as fin:
        for line in fin.readlines() [-1:]:
            readings = line.strip().split()
            if len(readings) != 8:
                continue;
            
            mytime.append(datetime.strptime(readings[0]+" "+readings[1], "%Y-%m-%d %H:%M:%S"))
            mysecs.append((mytime[-1]-mytime[0]).total_seconds()/60.)
            mytemp1.append(float(readings[2]))
            mytemp2.append(float(readings[3]))
            mytemp3.append(float(readings[4]))
            mytemp4.append(float(readings[5]))
            mytemp5.append(float(readings[6]))
            mytemp6.append(float(readings[7]))
            mytemp33.append(mytemp3[-1]-0.5*(mytemp1[-1]+mytemp2[-1]))
            mytemp44.append(mytemp4[-1]-0.5*(mytemp1[-1]+mytemp2[-1]))
            mytemp55.append(mytemp5[-1]-0.5*(mytemp1[-1]+mytemp2[-1]))
            mytemp66.append(mytemp6[-1]-0.5*(mytemp1[-1]+mytemp2[-1])) 
            print(str(readings[1])+" "+str(readings[2])+" "+str(readings[3])+" "+str(readings[4])+" "+str(readings[5])+" "+str(readings[6])+" "+str(readings[7]))
            
            graph()
            plt.pause(3)

