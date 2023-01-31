#!/bin/bash

#Join Zerotier Network
sudo zerotier-cli join $1
echo HOSTNAME=$HOTSNAME > .env

#Deploy
sudo docker-compose up -d