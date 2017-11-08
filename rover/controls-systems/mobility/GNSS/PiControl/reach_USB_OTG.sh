#!/bin/bash

sudo iptables -t nat -A POSTROUTING -s 192.168.2.0/24 -j MASQUERADE
### BEGIN INIT INFO
# Provides:          startup forwarding service for Ethernet Over USB
# Required-Start:    
# Required-Stop:     
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Reach system requirement for network communication
# Description:       This script will run the needed commands for the 
#                    Emlid Reach GNSS system at startup.
### END INIT INFO

# Author: Timothy Parks
