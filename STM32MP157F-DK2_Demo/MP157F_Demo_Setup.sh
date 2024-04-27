#!/bin/bash

apt-get update
apt-get upgrade -y
apt-get install python3-pip -y
dd if=/dev/zero of=/swapfile bs=1024 count=1048576
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
pip3 install bleak
cp -r /media/usbdrive/STM32MP157F-DK2_Demo /home/weston
cd /home/weston/STM32MP157F-DK2_Demo/iotconnect-python-sdk-v1.0/iotconnect-sdk-1.0
python3 setup.py install
pip3 install paho-mqtt==1.6.1
cd /home/weston/STM32MP157F-DK2_Demo
pip3 install blue_st_sdk-1.5.0-py3-none-any.whl
cp /home/weston/STM32MP157F-DK2_Demo/iotconnect.service /etc/systemd/system
systemctl enable iotconnect
