# HamRadioTCP-IP

> Prepared by Richard Stanley <br>
> AKA: Audstanley <br>
> Computer Science Major <br>
> Outside help from: [Steve Netting](http://www.m0spn.co.uk/), and [Mark Khusid](http://markkhusid.ddns.net/index.html)

-----

![Ham Radio Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/International_amateur_radio_symbol.svg/170px-International_amateur_radio_symbol.svg.png)


## Description:
The purpose of this function is to connect to the Titan Rover via the ax.25 protocol that is available through the Linux Kernel. This protocol acts similar to wlan0 or eth0 (aka wifi or ethernet). With ax.25 set up correctly on a raspberry pi 3 with a TNC-Pi2 "hat" at the base station, and a TNC-x on the rover, the two systems should be able to communicate on a designated frequency.  Depending on the frequency, there is a kilohertz spread.  If my memory serves me correctly, typically 5kHz on VHF.

So far, I've ordered a tnc-x that should be shipped soon.  It actually doesn't seem that ax.25 is very difficult to operate.  The raspberry pi installation manual for a TNCPi2 can be found [here](http://tnc-x.com/TNCPi.pdf), and I'll just need to setup a startup script for the raspberry pi on launch.  The tnc-x, which will be attached to the rover has an FTDI usb to serial built into the tnc-x, so it is completely compatible with Linux.

-----

### Concerns

Since the rules of ham radio explicitly state that radio operators are not allowed to encrypt data over ham radio frequencies, telnet would allow plain text data to be transmitted.  Although this posses potential security threats, it is unlikely that telnet would be compromised considering that in the competition the Titan Rover team will be on a wifi network that would be connected to the Rover (this network would/could be encrypted), so no access to the rover's telnet would be available to a malicious party.

It seems even **more** unlikely that there would be a malicious party that would have a similar setup scanning radio frequencies to pin point the data signal being transferred between TNCs. Not to mention they would have to spoof the call sign of the ax.25 protocol, which would be difficult, and not to mention illegal.  Therefore, I believe that there is no cause for grave concern on the matter of telnet security should the issue be raised among engineers.

Once you run kissattach, and set the two radios to the same frequencies, everything should be straight forward.  We will just need to run through installation of telnet server on the side of the rover.

-----

<br>

## Resources
### Ham Radio:

  * [RF Basics, RF for Non-RF Engineers](https://goo.gl/fMg5Dk)
  * [TNCPi2](http://tnc-x.com/TNCPi.htm)
  * [TNC-x](http://tnc-x.com/)
  * [5-Pin Din DIY Connector for TNC-X to Baofeng Radio](http://tnc-x.com/Baofeng.htm)
    * In the picture at the bottom of the page, you will see a baofeng connector (to the radio) to a DB9 connector. This connects to the TNCPi2 (not the tnc-x) Basically, I've ordered [two handheld mics](https://www.amazon.com/Original-Universal-Handheld-BAOFENG-Speaker-mic/dp/B00CIOA89E/ref=sr_1_2?s=hi&ie=UTF8&qid=1504629968&sr=8-2&keywords=baofeng+mic), chopped off the mic part, and one cable will have a [DB9](https://www.amazon.com/DealMux-Converter-Connector-Adapter-Assembly/dp/B072MTCYKL/ref=sr_1_50?s=hi&ie=UTF8&qid=1504629931&sr=1-50&keywords=db9) on one end and a baofeng radio on the other, and the second cable has a [5-Pin Din](https://www.amazon.com/NEUTRIK-NYS322-CONNECTOR-PLUG-5POS/dp/B003GZRCCK/ref=sr_1_4?ie=UTF8&qid=1504629531&sr=8-4&keywords=5+pin+din) on one end and a baofeng radio on the other.

### Ax.25 protocol:
  * [AX25-HOWTO.pdf](https://goo.gl/PMm9KV)

### Videos:
  * [ax.25 ssh by Steve Netting](https://www.youtube.com/watch?v=qdayzRIPEMk)
    * I've reached out to steve, and got his email address. He might be able to help out if there are any caveats along the way. Ont thing steve pointed out, is to disable any auto discovery services (such as samba).  Disabling samba will greatly reduce any unnecessary "noise" that would occur over the ax.25 protocol.
  * [ax.25 wireshark/packet sniffing by Mark Khusid](https://www.youtube.com/watch?v=_0h3SK5m9vk)
    * I have also reached out to Mark, and he has emailed me back on helping out we have any hangups.  He has been helpgul so far, here is his site [Mark's site](http://markkhusid.ddns.net/index.html)

  -----

  ![TncPi2](http://ww2.audstanley.com:8081/cpp/photos/PiTNC2.png)

  This is a photo I took of my TNCPi2 attached to a Baofeng handheld radio.