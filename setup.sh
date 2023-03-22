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

# Get Zerotier Node ID
NODE_ID=$(sudo zerotier-cli info | cut -d ' ' -f 3)

# Update Helper Scripts Permission
echo 'Configuring Wi-Fi...'
chmod +x scripts/*

# Run Helper Scripts
./scripts/wifi_setup.sh $wifi $ssid $pass

# Set Sudoer
echo 'Configuring Sudoers...'
sudo echo $USER 'ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Outro
echo -e '== Init Process Completed ==\n'
echo -e 'Your Node ID : '$NODE_ID'\n'
echo -e 'Use the ID to continue setup process\n'
echo -e '== Please Continue Setup Process from Server UI =='