#!/bin/bash

if pgrep -x "wlsunset" > /dev/null
then
    pkill wlsunset > /dev/null 2>&1
else
    wlsunset -t 3200
fi