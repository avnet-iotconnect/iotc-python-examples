#!/bin/bash

sudo apt-get update

echo "" >> /etc/network/interfaces
echo "auto enp1s0" >> /etc/network/interfaces
echo "iface enp1s0 inet dhcp" >> /etc/network/interfaces
echo "	dns-nameservers 8.8.8.8" >> /etc/network/interfaces
echo "" >> /etc/network/interfaces
echo "auto eth0" >> /etc/network/interfaces
echo "iface eth0 inet static" >> /etc/network/interfaces
echo "        address 169.254.169.2" >> /etc/network/interfaces
echo "        gateway 169.254.169.1" >> /etc/network/interfaces

sudo apt install unzip nano python3-pip -y
cd /home/asus/PE100_Demo
wget https://help.iotconnect.io/wp-content/uploads/2023/01/iotconnect-python-sdk-v1.0.zip
unzip iotconnect-python-sdk-v1.0.zip
cd iotconnect-python-sdk-v1.0
pip3 install iotconnect-sdk-1.0.tar.gz
pip3 install -U minimalmodbus pymodbus

sudo mkdir /media/usbdrive
echo -e "Please insert your flash drive with your certificates folder into a USB port on this device, wait 5 seconds, and then hit ENTER. "
read input
sudo mount /dev/sda1 /media/usbdrive || sudo mount /dev/sdb1 /media/usbdrive

cd /media/usbdrive
cp ./pk_PE100_Demo.pem ./cert_PE100_Demo.crt /home/asus/PE100_Demo

cd /home/asus/PE100_Demo/iotc-pov-engineering/PE100A_Motor_Monitor_Demo/
cp ./ADAM.py ./ModbusDevice.py ./PE100_Motor_Monitor_Demo.py /home/asus/PE100_Demo/iotconnect-python-sdk-v1.0/sample
cp ./root-CA.pem /home/asus/PE100_Demo

reboot


