#!/bin/bash

#Check Shell Argument
if [[ $# -eq 0 ]]
then
    echo 'No Zerotier ID supplied'
    exit 1
else

    #Join Zerotier Network
    sudo zerotier-cli join $1
    
    #Deploy
    docker-compose up -d
fi
