# HamRadioTCP-IP

> Prepared by Richard Stanley <br>
> AKA: Audstanley <br>
> Computer Science Major
-----

![Ham Radio Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/International_amateur_radio_symbol.svg/170px-International_amateur_radio_symbol.svg.png)


## Description:
The purpose of this function is to connect to the Titan Rover via the ax.25 protocol that is available through the Linux Kernel. This protocol acts similar to wlan0 or eth0 (aka wifi or ethernet). With ax.25 set up correctly on a raspberry pi 3 with a TNC-Pi2 "hat" at the base station, and a TNC-x on the rover, the two systems should be able to communicate on a designated frequency.  Depending on the frequency, there is a kilohertz spread.  If my memory serves me correctly, typically 5kHz on VHF, and  

-----

### Concerns

Since the rules of ham radio explicitly state that radio operators are not allowed to encrypt data over ham radio frequencies, telnet would allow plain text data to be transmitted.  Although this posses potential security threats, it is unlikely that telnet would be compromised considering that in the competition the Titan Rover team will be on a wifi network that would be connected to the Rover (this network would/could be encrypted), so no access to the rover's telnet would be available to a malicious party.

It seems even **more** unlikely that there would be a malicious party that would have a similar setup scanning radio frequencies to pin point the data signal being transferred between TNCs. Not to mention they would have to spoof the call sign of the ax.25 protocol, which would be difficult, and not to mention illegal.  Therefore, I believe that there is no cause for grave concern on the matter of telnet security should the issue be raised among engineers.   

-----

<br>

## Resources
### Ham Radio:

  * [RF Basics, RF for Non-RF Engineers](https://goo.gl/fMg5Dk)

### Ax.25 protocol:
  * [AX25-HOWTO.pdf](https://goo.gl/PMm9KV)

  -----

  ![TncPi2](http://ww2.audstanley.com:8081/cpp/photos/PiTNC2.png)

  This is a photo I took of my TNCPi2 attached to a Baofeng handheld radio.