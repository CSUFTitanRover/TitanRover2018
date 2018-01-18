file = open("/etc/udev/rule.d/serial-symlinks.rules", "w+")
file.write('SUBSYSTEM=="tty", ENV{ID_PATH}=="pci-0000:00:14.0-usb-0:2:1.2", SYMLINK+="tty-emlid"')
file.close