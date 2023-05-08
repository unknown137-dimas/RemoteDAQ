#!/bin/bash
sudo apt install -y make gcc bzip2 linux-headers-$(uname -r) kmod systemctl
sudo mkdir -p /lib/modules/$(uname -r)/kernel/drivers/daqnavi
sudo mkdir -p '/usr/local/lib/x86_64-linux-gnu'
sudo chmod +x daq-drivers/advantech/linux_driver_source_*_64bit.run
sudo ./daq-drivers/advantech/linux_driver_source_*_64bit.run silent install usb4702_usb4704
sudo apt purge -y make gcc bzip2 kmod
sudo apt autoremove -y