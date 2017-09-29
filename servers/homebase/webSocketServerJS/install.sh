#!/bin/bash
if [ "$EUID" -ne 0 ]
        then echo "You need to install as root by using sudo ./install.sh";
        exit
else
        sudo apt-get update;
        sudo apt-get install -y xboxdrv;
        echo "KERNEL==\"uinput\", MODE=\"0660\", GROUP=\"root\"" > /etc/udev/rules.d/55-permissions-uinput.rules;
fi
if [ "$(node -v)" != "v8.5.0" ]
        then echo "Current Version of node is already installed";
        wget -O - https://raw.githubusercontent.com/audstanley/NodeJs-Raspberry-Pi/master/Install-Node.sh | bash;
else
        echo "You are running the current version of NodeJs";
fi