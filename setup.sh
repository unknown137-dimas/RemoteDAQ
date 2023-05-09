#!/bin/bash

# Intro
echo '== Node Init Process Begin =='

# Script Options
wireless='false'

while getopts 'w' flag; do
    case "${flag}" in
        w) wireless='true' ;;
        *) wireless='false' ;;
    esac
done

# User Input
if $wireless; then
    read -p 'Input wireless interface: ' wifi
    read -p 'Input Wi-Fi network name: ' ssid
    read -sp 'Input Wi-Fi password: ' pass
fi
read -p 'Input ZeroTier network ID: ' zt_net_id

# Install Ansible
echo 'Installing Ansible...'
sudo apt install -y ansible > /dev/null 2>&1

if $wireless; then
    # Install WPA Supplicant
    echo 'Installing Wi-Fi Packages...'
    sudo apt update > /dev/null 2>&1
    sudo apt install -y wpasupplicant > /dev/null 2>&1

    # Update Helper Scripts Permission
    echo 'Configuring Wi-Fi...'
    chmod +x scripts/*

    # Setup Wi-Fi Network
    sudo ./scripts/wifi_setup.sh $wifi $ssid $pass
fi

# Install Zerotier Client
curl -s https://install.zerotier.com | sudo bash

# Join Zerotier Network
echo 'Connecting to ZeroTier Network...'
sudo zerotier-cli join $zt_net_id

# Get Zerotier Node ID
NODE_ID=$(sudo zerotier-cli info | cut -d ' ' -f 3)

# Outro
echo -e '== Init Process Completed ==\n'
echo -e 'Your Node ID : '$NODE_ID'\n'
echo -e 'Your Node ID : '$NODE_ID'\n' >> node_id.txt
echo -e 'Use the ID to continue setup process\n'
echo -e '== Please Continue Setup Process from Server UI =='