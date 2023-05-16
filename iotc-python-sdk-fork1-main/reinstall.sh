#!/bin/sh
echo "Uninstalling old SDK"
echo "---------------------------------"
pip3 uninstall iotconnect_sdk -y
echo ""
echo "Installing new SDK"
echo "---------------------------------"
pip3 install --user .
