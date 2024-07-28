#!/bin/bash

# KILLS ALL APP PROCESSES ON DEVICE (DOES NOT KILL SYSTEM PROCESSES)  

# Input source command
INPUT_SOURCE="frida-ps -Ua"

# Device ID
Device=$(frida-ls-devices | awk '/usb/{print $1}')

# Check Device ID 
if [ -z "$Device" ]; then
    echo "No USB device found."
    echo "Please Connect Device Via USB."
    exit 1
fi

# Command to run with PID
COMMAND_TO_RUN="frida-kill -D $Device"

# Read the PIDs into an array
PIDS=($($INPUT_SOURCE | awk 'NR>2 {print $1}'))

# Loop through the PIDs and execute the command for each
for pid in "${PIDS[@]}"
do
    # Execute the command with the current PID
    $COMMAND_TO_RUN $pid
    echo "killed $pid"  
done

