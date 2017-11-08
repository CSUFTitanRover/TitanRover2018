#!/bin/bash

HOST_USB_IP=192.168.2.2
TARGET_USB_UP=192.168.2.15
route add default gw $HOST_USB_IP
#ifconfig wlan0 down

