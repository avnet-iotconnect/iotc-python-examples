#!/bin/bash

cd iotconnect-python-sdk-v1.0
cd iotconnect-sdk-1.0
pip3 install --user .
sudo mkdir /media/usbdrive
echo -e "Please insert your flash drive with your certificates folder into a USB port on this device, and then hit ENTER. "
read input
sudo mount /dev/sda1 /media/usbdrive || sudo mount /dev/sdb1 /media/usbdrive

cp -r /media/usbdrive/STM32MP157_Demo-certificates /home/weston/Demo

cd /home/weston/Demo/iotc-pov-engineering-main/STM32MP157F-DK2_Demo/iotconnect-python-sdk-v1.0/sample