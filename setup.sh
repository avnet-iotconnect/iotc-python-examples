# Install python virtual environment
sudo apt install python3-venv
python3 -m venv .venv

# Download and install the IoTConnect SDK
wget https://github.com/avnet-iotconnect/iotc-python-sdk/archive/refs/heads/master-std-21.zip
unzip master-std-21.zip
.venv/bin/pip3 install iotc-python-sdk-master-std-21/iotconnect-sdk-1.0/

# Cleanup
rm master-std-21.zip 
rm -rf iotc-python-sdk-master-std-21/

echo "IoTConnect SDK Installed."

# # Install remaining python packages
# .venv/bin/pip3 install -r requirements.txt