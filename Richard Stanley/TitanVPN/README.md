# TitanVPN

I set up a raspberry pi virtual private network. I'm using [this](https://github.com/pivpn/pivpn). The Nvidia TX2 (brain) of the Rover is behind the school network, which poses a problem:  We can have the nvidia TX2 running 24/7 while connected to the internet, but there is no way to connect to the TX2 to install dependencies (for example connecting via ssh, or conecting to the desktop via VNC).

So I set the Nvidia TX2 up to connect to a private VPN server at my house. You can install an openVPN client on your [windows, linux](https://openvpn.net/index.php/open-source/downloads.html) or [mac](https://tunnelblick.net/) computer.

-----

## After installation of the clients (Links above)

Once you have openVPN client installed on your machine, you will need a certificate to log into the VPN network. Get in contact [with me on slack](https://titanrover.slack.com/messages/@audstanley/) and we will generate a certificate for you so you can get connected to the TX2.  This is for **developers** that need access to install dependencies, or test various things remotely and if you understand linux well enough to have a dedicated connection to the TX2, then this will help everyone that needs to write software.  If you are not Linux savvy, then this might be a good opportunity to learn.  Also, **you can break stuff** with access to the TX2 by installing things incorrectly.  So Tim and I may need to curate who does, and does not have VPN access (it's a real pain to get the TX2 flashed back to factory settings).  I'll leave the final decision on ***who*** has vpn access to Tim, and you can contact me first, if you are interested in having VPN access, so we can discuss the option.