#!/bin/bash

su
apt-get update
apt-get upgrade -y
apt-get install python3-pip -y
dd if=/dev/zero of=/swapfile bs=1024 count=1048576
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
pip3 install bleak
cp -r /media/usbdrive/PROTEUS_MP157F_Demo /home/weston
cd /home/weston/PROTEUS_MP157F_Demo/iotconnect-python-sdk-v1.0/iotconnect-sdk-v1.0
python3 setup.py install
(crontab -l 2>/dev/null; echo "@reboot python3 /home/weston/PROTEUS_MP157F_Demo/iotconnect-python-sdk-v1.0/sample/STM32MP157F-DK2_PROTEUS_Demo.py") | crontab -
