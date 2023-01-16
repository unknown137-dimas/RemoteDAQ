#!/bin/bash

#Install Zerotier Client
curl -s https://install.zerotier.com | sudo bash
zerotier-cli join $1

#Deploy
docker-compose up -d