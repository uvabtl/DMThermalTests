import sys
import time
import pyvisa as visa
import warnings
warnings.simplefilter(action = "ignore", category = UserWarning)

'''==========================================================================================================================================='''
'''==========================================================================================================================================='''

# This transmits the messages to the power supply that causes the changes to occur.
def command(command, vi):
    vi.write(command)

# This returns the state of the command.
def query(command, vi):
    return vi.query(command)

# This sets the default (active) channel.
def setActiveChannel(channel, vi):
    command("inst:nsel " + str(channel), vi)

# This turns on (1) and off (0) remote mode, depending on the state.
def remoteMode(state, vi):
    cmd = "syst:rem" if state else "syst:loc"
    command(cmd, vi)

# This turns on and off series mode.
def seriesMode(in_cmd, vi):
    command("inst:com:trac NONE", vi)
    command("inst:com:para NONE", vi)
    command(in_cmd, vi)
    cmd = "outp:ser?"
    query(cmd, vi)

# This turns on the channels (channel 1 == 1, channel 2 == 2, etc.).
def channelOn(channel, vi):
    setActiveChannel(channel, vi)
    command("outp on", vi)

# This is analogous to channelOn, but it turns off the channels.
def channelOff(channel, vi):
    setActiveChannel(channel, vi)
    command("outp off", vi)

# This sets any voltage of the chosen channel immediately to a value.
def setVoltage(volt, vi):
    cmd = "volt " + str(volt) + "V"
    command(cmd, vi)

# Not sure what this one does, either.
def queryVoltage(vi):
    cmd = "meas:volt?"
    print("Voltage in V currently at {0}".format(query(cmd, vi)), end = "")
    return query(cmd, vi)

# This tells you which channel is on.
def queryChannel(vi):
    cmd = "inst?"
    print("Channel set to {0}".format(query(cmd, vi)), end = "")
    return query(cmd, vi)

# This sets the voltage over a specified amount of time, so it ramps up.
def stepVolt(vi, v1, t = 5, dt = 0.25):
    v0 = float(queryVoltage(vi))
    nt = t / dt
    dv = (v1 - v0) / nt
    newV = v0
    for i in range(int(nt)):
        newV = newV + dv
        setVoltage(newV, vi)
        time.sleep(dt)
    setVoltage(v1, vi)

# This seems like it just tests various capabilities of the power supply.
def diagnostic(channel, vi):
    setActiveChannel(channel, vi)
    remoteMode(1, vi)   # Enables remote mode
    channelOn(channel, vi)    # Enables channel
    setVoltage(10, vi)
    time.sleep(3)
    queryVoltage(vi)
    stepVolt(vi, 24)          # Set voltage to 24 from 10, over 5 seconds
    time.sleep(3)

    stepVolt(vi, 30)          # Steps to 30V
    time.sleep(3)
    stepVolt(vi, 0)           # Steps to 0V
    time.sleep(3)

    channelOff(channel, vi)   # Disables channel
    remoteMode(0, vi)         # Disables remote mode
    
# This function sets on a channel of the user's choosing and tells you which is on.
def tryQuery(channel, vi):
    remoteMode(channel, vi)
    channelOn(channel, vi)
    queryChannel(vi)

def setCurrent(current, vi):
    cmd = "curr " + str(current) + "A"
    command(cmd, vi)
 
def queryCurrent(vi):
    cmd = "meas:curr?"
    print("Current in A currently at {0}".format(query(cmd, vi)), end = "")
    return query(cmd, vi)

def stepCurr(vi, c1, t = 5, dt = 0.25):
    c0 = float(queryCurrent(vi))
    nt = t / dt
    dc = (c1 - c0) / nt
    newC = c0
    for i in range(int(nt)):
        newC = newC + dc
        setCurrent(newC, vi)
        time.sleep(dt)
    setCurrent(c1, vi)

def queryPower(vi):
    cmd = "meas:pow?"
    print("Power in W currently at {0}".format(query(cmd, vi)), end = "")
    return query(cmd, vi)
    
'''==========================================================================================================================================='''
'''==========================================================================================================================================='''

rm = visa.ResourceManager()
li = rm.list_resources()

# This for loop tells you which ports are taken on the PC.
for index in range(len(li)):
    print(str(index) + " - " + li[index])
vi = rm.open_resource(li[0])
print("\nPort used by power supply: " + vi.query("syst:addr?"))   # Prints the system address (aka the port)

try:
    user_input = input("Start of program. Enter a function: ")
except KeyboardInterrupt:
    print("\nExiting. Any channels and modes that are currently on WILL REMAIN ON.")
    print("Goodbye.")
    sys.exit(1)
while (user_input.lower() != "exit"):
    try:
        if (user_input == "setActiveChannel"):
            channel_input = input("Channel: ")
            if (channel_input.lower() == "exit"):
                break
            elif (channel_input.lower() == "back"):
                pass
            else:
                while ((channel_input != "1") and (channel_input != "2") and (channel_input != "3")):
                    if (channel_input.lower() == "exit"):
                        print("Exiting. Any channels and modes that are currently on WILL REMAIN ON.")
                        print("Goodbye.")
                        sys.exit(1)
                    elif (channel_input.lower() == "back"):
                        break
                    else:
                        channel_input = input("Not an integer between 1 and 3. Try again: ")
                if (channel_input.lower() == "back"):
                    pass
                else:
                    setActiveChannel(int(channel_input), vi)
                    print("Done.", end = " ")
        elif (user_input == "remoteMode"):
            state_input = input("State: ")
            if (state_input.lower() == "exit"):
                break
            elif (state_input.lower() == "back"):
                pass
            else:
                while ((state_input != "0") and (state_input != "1")):
                    if (state_input.lower() == "exit"):
                        print("Exiting. Any channels and modes that are currently on WILL REMAIN ON.")
                        print("Goodbye.")
                        sys.exit(1)
                    elif (state_input.lower() == "back"):
                        break
                    else:
                        state_input = input("Not an integer between 0 and 1. Try again: ")
                if (state_input.lower() == "back"):
                    pass
                else:
                    remoteMode(int(state_input), vi)
                    print("Done.", end = " ")
        elif (user_input == "seriesMode"):
            state_input = input("State: ")
            if (state_input.lower() == "exit"):
                break
            elif (state_input.lower() == "back"):
                pass
            else:
                while ((state_input != "inst:com:ser") and (state_input != "inst:com:off")):
                    if (state_input.lower() == "exit"):
                        print("Exiting. Any channels and modes that are currently on WILL REMAIN ON.")
                        print("Goodbye.")
                        sys.exit(1)
                    elif (state_input.lower() == "back"):
                        break
                    else:
                        state_input = input("Not \"inst:com:ser\" or \"inst:com:off.\" Try again: ")
                if (state_input.lower() == "back"):
                    pass
                else:
                    seriesMode(state_input, vi)
                    print("Done.", end = " ")
        elif (user_input == "channelOn"):
            channel_input = input("Channel: ")
            if (channel_input.lower() == "exit"):
                break
            elif (channel_input.lower() == "back"):
                pass
            else:
                while ((channel_input != "1") and (channel_input != "2") and (channel_input != "3")):
                    if (channel_input.lower() == "exit"):
                        print("Exiting. Any channels and modes that are currently on WILL REMAIN ON.")
                        print("Goodbye.")
                        sys.exit(1)
                    elif (channel_input.lower() == "back"):
                        break
                    else:
                        channel_input = input("Not an integer between 1 and 3. Try again: ")
                if (channel_input.lower() == "back"):
                    pass
                else:
                    channelOn(int(channel_input), vi)
                    print("Done.", end = " ")
        elif (user_input == "channelOff"):
            channel_input = input("Channel: ")
            if (channel_input.lower() == "exit"):
                break
            elif (channel_input.lower() == "back"):
                pass
            else:
                while ((channel_input != "1") and (channel_input != "2") and (channel_input != "3")):
                    if (channel_input.lower() == "exit"):
                        print("Exiting. Any channels and modes that are currently on WILL REMAIN ON.")
                        print("Goodbye.")
                        sys.exit(1)
                    elif (channel_input.lower() == "back"):
                        break
                    else:
                        channel_input = input("Not an integer between 1 and 3. Try again: ")
                if (channel_input.lower() == "back"):
                    pass
                else:
                    channelOff(int(channel_input), vi)
                    print("Done.", end = " ")
        elif (user_input == "tryQuery"):
            channel_input = input("Channel: ")
            if (channel_input.lower() == "exit"):
                break
            elif (channel_input.lower() == "back"):
                pass
            else:
                while ((channel_input != "1") and (channel_input != "2") and (channel_input != "3")):
                    if (channel_input.lower() == "exit"):
                        print("Exiting. Any channels and modes that are currently on WILL REMAIN ON.")
                        print("Goodbye.")
                        sys.exit(1)
                    elif (channel_input.lower() == "back"):
                        break
                    else:
                        channel_input = input("Not an integer between 1 and 3. Try again: ")
                if (channel_input.lower() == "back"):
                    pass
                else:
                    tryQuery(int(channel_input), vi)
                    print("Done.", end = " ")
        elif (user_input == "diagnostic"):
            channel_input = input("Channel: ")
            if (channel_input.lower() == "exit"):
                break
            elif (channel_input.lower() == "back"):
                pass
            else:
                while ((channel_input != "1") and (channel_input != "2") and (channel_input != "3")):
                    if (channel_input.lower() == "exit"):
                        print("Exiting. Any channels and modes that are currently on WILL REMAIN ON.")
                        print("Goodbye.")
                        sys.exit(1)
                    elif (channel_input.lower() == "back"):
                        break
                    else:
                        channel_input = input("Not an integer between 1 and 3. Try again: ")
                if (channel_input.lower() == "back"):
                    pass
                else:
                    diagnostic(int(channel_input), vi)
                    print("Done.", end = " ")
        elif (user_input == "setVoltage"):
            voltage_input = input("Voltage: ")
            if (voltage_input.lower() == "exit"):
                break
            elif (voltage_input.lower() == "back"):
                pass
            else:
                try:
                    float(voltage_input)
                except ValueError:
                    if (voltage_input.lower() == "exit"):
                        print("Exiting. Any channels and modes that are currently on WILL REMAIN ON.")
                        print("Goodbye.")
                        sys.exit(1)
                    elif (voltage_input.lower() == "back"):
                        break
                    else:
                        voltage_input = input("Not a number between 0 and 20. Try again: ")
                if (voltage_input.lower() == "back"):
                    pass
                else:
                    while (voltage_input.startswith("-") or (float(voltage_input) > 20.0)):
                        if (voltage_input.lower() == "exit"):
                           print("Exiting. Any channels and modes that are currently on WILL REMAIN ON.")
                           print("Goodbye.")
                           sys.exit(1)
                        elif (voltage_input.lower() == "back"):
                           break
                        else:
                           voltage_input = input("Not a number between 0 and 20. Try again: ")
                    if (voltage_input.lower() == "back"):
                        pass
                    else:
                        setVoltage(float(voltage_input), vi)
                        print("Done.", end = " ")
        elif (user_input == "stepVolt"):
            voltage_input = input("Voltage: ")
            if (voltage_input.lower() == "exit"):
                break
            elif (voltage_input.lower() == "back"):
                pass
            else:
                try:
                    float(voltage_input)
                except ValueError:
                    if (voltage_input.lower() == "exit"):
                        print("Exiting. Any channels and modes that are currently on WILL REMAIN ON.")
                        print("Goodbye.")
                        sys.exit(1)
                    elif (voltage_input.lower() == "back"):
                        break
                    else:
                        voltage_input = input("Not a number between 0 and 20. Try again: ")
                if (voltage_input.lower() == "back"):
                    pass
                else:
                    while (voltage_input.startswith("-") or (float(voltage_input) > 20.0)):
                        if (voltage_input.lower() == "exit"):
                           print("Exiting. Any channels and modes that are currently on WILL REMAIN ON.")
                           print("Goodbye.")
                           sys.exit(1)
                        elif (voltage_input.lower() == "back"):
                           break
                        else:
                           voltage_input = input("Not a number between 0 and 20. Try again: ")
                    if (voltage_input.lower() == "back"):
                        pass
                    else:
                        stepVolt(vi, float(voltage_input))
                        print("Done.", end = " ")
        elif (user_input == "queryVoltage"):
            queryVoltage(vi)
            print("Done.", end = " ")
        elif (user_input == "queryChannel"):
            queryChannel(vi)
            print("Done.", end = " ")
        elif (user_input == "setCurrent"):
            current_input = input("Current: ")
            if (current_input.lower() == "exit"):
                break
            elif (current_input.lower() == "back"):
                pass
            else:
                try:
                    float(current_input)
                except ValueError:
                    if (current_input.lower() == "exit"):
                        print("Exiting. Any channels and modes that are currently on WILL REMAIN ON.")
                        print("Goodbye.")
                        sys.exit(1)
                    elif (current_input.lower() == "back"):
                        break
                    else:
                        current_input = input("Not a number between 0 and 0.25. Try again: ")
                if (current_input.lower() == "back"):
                    pass
                else:
                    while (current_input.startswith("-") or (float(current_input) > 0.25)):
                        if (current_input.lower() == "exit"):
                           print("Exiting. Any channels and modes that are currently on WILL REMAIN ON.")
                           print("Goodbye.")
                           sys.exit(1)
                        elif (current_input.lower() == "back"):
                           break
                        else:
                           current_input = input("Not a number between 0 and 0.25. Try again: ")
                    if (current_input.lower() == "back"):
                        pass
                    else:
                        setCurrent(float(current_input), vi)
                        print("Done.", end = " ")
        elif (user_input == "stepCurr"):
            current_input = input("Current: ")
            if (current_input.lower() == "exit"):
                break
            elif (current_input.lower() == "back"):
                pass
            else:
                try:
                    float(current_input)
                except ValueError:
                    if (current_input.lower() == "exit"):
                        print("Exiting. Any channels and modes that are currently on WILL REMAIN ON.")
                        print("Goodbye.")
                        sys.exit(1)
                    elif (current_input.lower() == "back"):
                        break
                    else:
                        current_input = input("Not a number between 0 and 0.25. Try again: ")
                if (current_input.lower() == "back"):
                    pass
                else:
                    while (current_input.startswith("-") or (float(current_input) > 0.25)):
                        if (current_input.lower() == "exit"):
                           print("Exiting. Any channels and modes that are currently on WILL REMAIN ON.")
                           print("Goodbye.")
                           sys.exit(1)
                        elif (current_input.lower() == "back"):
                           break
                        else:
                           current_input = input("Not a number between 0 and 0.25. Try again: ")
                    if (current_input.lower() == "back"):
                        pass
                    else:
                        stepCurr(vi, float(current_input))
                        print("Done.", end = " ")
        elif (user_input == "queryCurrent"):
            queryCurrent(vi)
            print("Done.", end = " ")
        elif (user_input == "queryPower"):
            queryPower(vi)
            print("Done.", end = " ")
        else:
            user_input = input("Not a function that exists. Try again: ")
            continue
        user_input = input("Enter a function: ")
    except KeyboardInterrupt:
        print("\n", end = "")
        break
print("Exiting. Any channels and modes that are currently on WILL REMAIN ON.")
print("Goodbye.")
