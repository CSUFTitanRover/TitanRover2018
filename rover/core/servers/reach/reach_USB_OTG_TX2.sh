#!/bin/bash

#IP Forwarding command for reach communication
iptables -t nat -A POSTROUTING -s 192.168.2.0/24 -j MASQUERADE

#Don't forget ---  chmod +x reach_USB_OTG_TX2.sh
