Reach System Requirements for Network Communications
=============================================================================================================
This system will enable the network packet forwarding between the Rasberry Pi and the Reach Via the USB cable


TX2 - Required Changes:
================================

Run bash command once:

    echo "1" > /proc/sys/net/ipv4/ip_forward

=============

ADD to /etc/network/interface file

    allow-hotplug usb0
    auto usb0
    iface usb0 inet static
        address 192.168.2.2
        netmask 255.255.255.0


=============

Startup script "reach_USB_OTG_TX2.sh" required on Rover TX2

    #Bash Commands in script
    iptables -t nat -A POSTROUTING -s 192.168.2.0/24 -J MASQUERADE


Emlid Reach ON ROVER CONNECTED TO TX2 VIA USB - Required Changes:
================================

Startup script "reach_USB_OTG_Reach.sh" required on Rover Emlid Reach

    #Bash Commands in script
    HOST_USB_IP=192.168.2.2
    TARGET_USB_UP=192.168.2.15
    route add default gw $HOST_USB_IP


