#!/bin/bash

#User Input
read -p 'Input wireless interface: ' wifi
read -p 'Input Wi-Fi network name: ' ssid
read -sp 'Input wifi password: ' pass

#Create wpa_supplicant.conf File
sudo wpa_passphrase $ssid $pass  | sudo tee /etc/wpa_supplicant.conf

#Create wpa_supplicant.service File
cat <<EOF > wpa_supplicant.service
[Unit]
Description=WPA supplicant
Before=network.target systemd-networkd.service
After=dbus.service
Wants=network.target
IgnoreOnIsolate=true

[Service]
Type=dbus
BusName=fi.w1.wpa_supplicant1
ExecStart=/sbin/wpa_supplicant -u -s -c /etc/wpa_supplicant.conf -i $wifi
Restart=always
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
EOF

#Create dhclient.service File
cat <<EOF > dhclient.service
[Unit]
Description= DHCP Client
Before=network.target
After=wpa_supplicant.service

[Service]
Type=forking
ExecStart=/sbin/dhclient $wifi -v
ExecStop=/sbin/dhclient $wifi -r
Restart=always

[Install]
WantedBy=multi-user.target
EOF

#Copy wpa_supplicant.service & dhclient.service File
sudo cp wpa_supplicant.service /etc/systemd/system/wpa_supplicant.service
sudo cp dhclient.service /etc/systemd/system/dhclient.service

#Reload Systemd
sudo systemctl daemon-reload

#Enable Service
sudo systemctl enable wpa_supplicant.service
sudo systemctl enable dhclient.service

#Cleanup
rm *.service