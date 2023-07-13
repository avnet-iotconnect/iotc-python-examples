#!/bin/bash

sudo apt-get update

sudo apt install unzip python3-pip -y
cd /home/asus/PE100_Demo
# wget https://help.iotconnect.io/wp-content/uploads/2023/01/iotconnect-python-sdk-v1.0.zip
wget https://github.com/avnet-iotconnect/iotc-python-sdk/archive/refs/heads/master-std-21.zip
# unzip iotconnect-python-sdk-v1.0.zip
unzip master-std-21.zip
# cd iotconnect-python-sdk-v1.0
cd iotc-python-sdk-master-std-21
pip3 install iotconnect-sdk-1.0.tar.gz

sudo mkdir /media/usbdrive
echo -e "Please insert your flash drive with your certificates folder into a USB port on this device, wait 5 seconds, and then hit ENTER. "
read input
sudo mount /dev/sda1 /media/usbdrive || sudo mount /dev/sdb1 /media/usbdrive

cp -r /media/usbdrive/PE100_Demo-certificates /home/asus/PE100_Demo

cd /home/asus/PE100_Demo/iotc-pov-engineering/PE100A_Basic_AWS_Demo/
cp ./PE100_Basic_Demo.py /home/asus/PE100_Demo/iotc-python-sdk-master-std-21/sample
cp ./root-CA.pem /home/asus/PE100_Demo


