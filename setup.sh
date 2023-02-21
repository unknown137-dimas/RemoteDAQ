#!/bin/bash

echo '== Node Init Process Begin =='

# User Input
read -p 'Input wireless interface: ' wifi
read -p 'Input Wi-Fi network name: ' ssid
read -sp 'Input Wi-Fi password: ' pass
read -p 'Input ZeroTier network ID: ' zt_net_id

# Install WPA Supplicant
echo 'Installing Wi-Fi Packages...'
sudo apt update > /dev/null 2>&1
sudo apt install -y wpasupplicant > /dev/null 2>&1

# Install Zerotier Client
curl -s https://install.zerotier.com | sudo bash

# Install Ansible
echo 'Installing Ansible...'
sudo apt install -y ansible > /dev/null 2>&1

# Join Zerotier Network
echo 'Connecting to ZeroTier Network...'
sudo zerotier-cli join $zt_net_id

# Update Helper Scripts Permission
echo 'Configuring Wi-Fi...'
chmod +x scripts/*

# Run Helper Scripts
./scripts/wifi_setup.sh $wifi $ssid $pass

# Set Sudoer
echo 'Configuring Sudoers...'
sudo echo $USER 'ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

echo '== Init Process Completed =='
echo '== Please Continue Setup Process from Server UI =='