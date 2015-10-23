#!/bin/bash
if ! [ "$(ping -c 1 www.google.com)" ]; then
    ifdown wlan0
    ifup wlan0
fi 

