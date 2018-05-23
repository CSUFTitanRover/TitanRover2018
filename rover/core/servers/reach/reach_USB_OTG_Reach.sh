#!/bin/bash

#IP Forwarding commands required on boot
HOST_USB_IP=192.168.2.2
TARGET_USB_UP=192.168.2.15
route add default gw $HOST_USB_IP

#Don't forget ---  chmod +x reach_USB_OTG_TX2.sh
