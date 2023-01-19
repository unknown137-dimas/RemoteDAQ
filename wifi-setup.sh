#!/bin/bash

#Check Shell Argument
if [[ $# -eq 0 ]]
then
    echo 'No wireless interface supplied'
    exit 1
else

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
    ExecStart=/sbin/wpa_supplicant -u -s -c /etc/wpa_supplicant.conf -i $1
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
    ExecStart=/sbin/dhclient $1 -v
    ExecStop=/sbin/dhclient $1 -r
    Restart=always

    [Install]
    WantedBy=multi-user.target
EOF

    #Copy wpa_supplicant.service File
    sudo cp wpa_supplicant.service /etc/systemd/system/wpa_supplicant.service

    #Reload systemd
    sudo systemctl daemon-reload

    #Enable Service
    sudo systemctl enable wpa_supplicant.service
    sudo systemctl enable dhclient.service
fi
