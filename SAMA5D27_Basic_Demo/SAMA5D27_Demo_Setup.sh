#!/bin/bash
cd /home/root/SAMA5D27_Basic_Demo/iotconnect-python-sdk-v1.0/iotconnect-sdk-1.0
python3 setup.py install
pip3 install paho-mqtt==1.6.1
cp /home/root/SAMA5D27_Basic_Demo/iotconnect.service /etc/systemd/system
systemctl enable iotconnect
