
Add persistant /dev/tty-emlid port on the machine to always connect to /dev/tty-emlid

## Instructions to do so:

```
go to /etc/udev/rule.d/ and create a file "serial-symlinks.rules" and add the following lines

SUBSYSTEM=="tty", ENV{ID_PATH}=="pci-0000:00:14.0-usb-0:2:1.2", SYMLINK+="tty-emlid"
```

save the file

===========================

## On the GNSS rover sensor add following lines to /etc/profile

```
#!/bin/sh
ifconfig wlan0 down
ifconfig
exit
  
####NOTE##### >>>> Doing this kicks you out if you try to ssh into the sensor. To recover from that just use command ssh root@192.168.2.15 "rm /etc/profile"
```
save the file 

===========================


## For Correction Input from Base Reach to Rover Reach follow the below steps

>go to base rover **webpage (192.168.1.117)** --> navigate to **base mode** ---> in the **corrections output section** --> Choose **TCP** --> role = **client** , Address = **ip address of the machine you want to forward**, port = **9000**

apply the settings

===========================
