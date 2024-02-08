#!/bin/bash

while true; do
    echo "Have you set up wifi on this device before and just need to change the SSID/Password? Type 'Y' for YES or 'N' for NO and then press ENTER"
    read response
    if [ "$response" != "N" -a  "$response" != "Y"]; then
       echo "Entry must be Y or N"
       continue # Go to the top of the loop
    fi
    break # Valid input given so exit the loop.
done

if [ "$response" == "N" ]; then
    ifconfig wlan0 up
    echo "[Match]" > /lib/systemd/network/51-wireless.network
    echo "Name=wlan0" >> /lib/systemd/network/51-wireless.network
    echo "[Network]" >> /lib/systemd/network/51-wireless.network
    echo "DHCP=ipv4" >> /lib/systemd/network/51-wireless.network
    mkdir -p /etc/wpa_supplicant/
    echo "ctrl_interface=/var/run/wpa_supplicant" > /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
    echo "eapol_version=1" >> /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
    echo "ap_scan=1" >> /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
    echo "fast_reauth=1" >> /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
    echo "" >> /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
fi

while true; do
    echo "Please type your wireless network name, also known as the SSID, and press ENTER"
    read ssid
    if [ -z $ssid ]; then
       echo "SSID cannot be empty"
       continue # Go to the top of the loop
    fi
    break # Valid input given so exit the loop.
done

while true; do
    echo "Please type the password of this SSID and press ENTER"
    read password
    if [ -z $password ]; then
       echo "Password cannot be empty"
       continue # Go to the top of the loop
    fi
    break # Valid input given so exit the loop.
done

wpa_passphrase $ssid $password >> /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
if [ "$response" == "N" ]; then
    systemctl enable wpa_supplicant@wlan0.service
fi
systemctl restart systemd-networkd.service
systemctl restart wpa_supplicant@wlan0.service
