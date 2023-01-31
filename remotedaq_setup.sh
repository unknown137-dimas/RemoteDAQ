#!/bin/bash

#User Input
read -p 'Input wireless interface: ' wifi
read -p 'Input Wi-Fi network name: ' ssid
read -sp 'Input Wi-Fi password: ' pass
read -p 'Input ZeroTier network ID: ' ztid

#Update Helper Scripts Permission
chmod +x scripts/*

#Run Helper Scripts
./scripts/wifi_setup.sh $wifi $ssid $pass
./scripts/install.sh
./scripts/deploy.sh $ztid