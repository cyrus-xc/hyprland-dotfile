#!/bin/bash

if pgrep -x "wlsunset" > /dev/null
then
    pkill wlsunset > /dev/null 2>&1
else
    wlsunset -T 4500
fi