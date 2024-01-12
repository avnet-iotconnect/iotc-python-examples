This is a demo to add Lorawan functionality to IOTConnect using the Python SDK on a STM32MP157 evaluation board.
The Python SDK bridges the Chirpstack Lora Network Server to IOTConnect.

IOTConnect and Chirpstack have different hierarchies, the current demo replicates the three tier hierarchy on IOTConnect.

A Lora Network Server (LNS) becomes an IOTConnect Gateway device
Lora Concentrators (LC) (or Gateways) become children of the the LNS device.

Each Chirpstack Application (CA) gets its own IOTConnect Gateway device, and the children of the CA become the Gateway's children.

This uses a kirkstone yocto build

## Build Instructions

This demo leverages the power of Docker to create a reproducible build that works across different OS environments, one of the main ideas is to avoid problems caused by having a too old/new version of Linux being used the Yocto build system, as those can cause build failures.

Tested on Ubuntu 22.04, 23.04, Kubuntu 22.04

# Requirements
- Repo tool (from Google) - https://android.googlesource.com/tools/repo
- Docker - https://docs.docker.com/engine/install/ubuntu/ + https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user
- git name and email added to global scope
- STM32_Programmer_CLI (added to path as well) for flashing

# Method
1. Create a work directory, for example ~/work
    ```bash
    cd ~/work
    ```

2. Create project directory and enter it
    ```bash
    mkdir STM32MP15-kirkstone && cd STM32MP15-kirkstone
    ```

3. Use repo tool to get stm32 yocto sources
    ```bash
    repo init -u https://github.com/STMicroelectronics/oe-manifest.git -b refs/tags/openstlinux-5.15-yocto-kirkstone-mp1-v23.07.26 && repo sync
    ```

4.  Copy provided Makefile to project directory and execute these commands in the terminal
    ```bash
    make docker
    ```

5.  Create a new terminal on the host machine:
    ```bash
    # this will install the extra dependencies we need
    docker exec -u root $(docker ps --filter "ancestor=crops/poky:ubuntu-22.04" --format "{{.Names}}") apt-get -y install bsdmainutils libgmp-dev libmpc-dev libssl-dev python3-pip
    # return back to the terminal where you executed the last step.
    ```

6.  Inside the docker container execute: 
    ```bash
    DISTRO=openstlinux-weston MACHINE=stm32mp1 source layers/meta-st/scripts/envsetup.sh
    # go through the EULA and accept everything.
    
    exit
    make build
    # this will take a while as this is the initial build.
    ```

5.  Now we will need to add the Yocto Python SDK layers (note that the repo is a fork and the contents of the repository may change as the demo progresses)

    ```bash
    # from the root project directory on the host machine
    cd layers
    git clone https://github.com/pywtk/iotc-yocto-python-sdk.git -b kirkstone-lora meta-iotconnect

    cd meta-st
    git clone https://github.com/akarnil/meta-st-stm32mpu-app-lorawan.git -b kirkstone

    cd ../../

    make env
    bitbake-layers add-layer ../layers/meta-st/meta-st-stm32mpu-app-lorawan
    bitbake-layers add-layer ../layers/meta-iotconnect/meta-iotc-python-sdk
    bitbake-layers add-layer ../layers/meta-iotconnect/meta-my-iotc-python-sdk-example
    exit

    make build
    ```

6. To flash (unfinished)
    ```bash
    make flash
    ``````


