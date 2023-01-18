#!/bin/bash
apt update
apt install -y make gcc bzip2 linux-headers-$(uname -r) kmod systemctl
mkdir -p /lib/modules/$(uname -r)/kernel/drivers/daqnavi
mkdir -p '/usr/local/lib/x86_64-linux-gnu'
./daq-drivers/advantech/linux_driver_source_*_64bit.run silent install usb4702_usb4704
apt purge -y make gcc bzip2 linux-headers-$(uname -r) kmod
apt autoremove -y