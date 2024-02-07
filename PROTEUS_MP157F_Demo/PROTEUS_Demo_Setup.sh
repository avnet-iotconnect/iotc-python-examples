#!/bin/bash

apt-get update
apt-get upgrade -y
apt-get install python3-pip -y
dd if=/dev/zero of=/swapfile bs=1024 count=1048576
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
pip3 install bleak
cp -r /media/usbdrive/PROTEUS_MP157F_Demo /home/weston
cd /home/weston/PROTEUS_MP157F_Demo/iotconnect-python-sdk-v1.0/iotconnect-sdk-1.0
python3 setup.py install
