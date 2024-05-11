#!/bin/bash

# Source the red_variable.sh script to get the variable
source ~/.config/waybar/scripts/red_variable.sh

# Check if the variable is set. If not, set it to 0
if [ -z "$VAR" ]
then
    VAR=0
fi

# Increase the variable by 100
VAR=$((VAR + 200))

# Update the variable in red_variable.sh
echo "VAR=$VAR" > ~/.config/waybar/scripts/red_variable.sh

# Print the new value of VAR
echo "New value of VAR: $VAR"

# Check if wlsunset is running
if pgrep -x "wlsunset" > /dev/null
then
    # If wlsunset is running, kill it
    pkill -9 "wlsunset"
fi

# Run wlsunset with the new value
wlsunset -t $VAR