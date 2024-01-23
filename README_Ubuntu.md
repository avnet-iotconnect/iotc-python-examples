# IoTConnect Ubuntu Python Demos

This is a collection of demos that (should) run on any gateway running Ubuntu. 

Here is a list of gateways that have been tested:
* DELL 3200/5200


## Step 0: Pre-requisites
This demo assumes the following:
* You have an existing IoTConnect account on AWS (Register for a free account on the [Subscription Page](https://subscription.iotconnect.io/subscribe)) 
* You have a github account with access to 
* You have a gateway, mouse, keyboard, and monitor with a display port cable.
* The gateway is running Ubuntu. If the device needs to be re-flashed follow [this guide](https://www.dell.com/support/manuals/en-do/dell-edge-gateway-3200/egw-3200-software-users-guide/create-bootable-usb-stick-for-restore?guid=guid-6ec73f04-322f-4795-88fa-dea90eb9e8bb&lang=en-us)

## Step 1: 
* Plug in the device using it's provided power adapter and power it on.
* Plug in your mouse, keyboard, and monitor to the gateway.
* Follow the prompts from Ubuntu to setup the OS and create a user profile. **Make sure to remember your credentials**
* Once you are on the desktop 

## Step 2: Download the demo repository
* Open the terminal and run the following command to download and unzip this repostiory:

      wget https://github.com/avnet-iotconnect/iotc-ubuntu-python-demos/archive/refs/heads/main.zip
      unzip iotc-ubuntu-python-demos-main.zip
  
## Step 3: Setup and Run a Demo
* Run the `setup.sh` script in the terminal to install the latest version of the IoTConnect SDK in a python virtual environment

This repository comes with the following demos:
* basic_demo
  
Navigate to the directory of the demo you would like to run and follow the instructions on the README to get it setup and running.
