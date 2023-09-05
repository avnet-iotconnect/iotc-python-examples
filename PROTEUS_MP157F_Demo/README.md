# PROTEUS / STM32MP157F-DK2 Demo (For IoTConnect on AWS)

This demo uses an [Discovery kit with STM32MP157F MPU](https://www.st.com/en/evaluation-tools/stm32mp157f-dk2.html) to run an IoTConnect program to monitor precise telemetry data in real-time on the IoTConnect cloud platform using AWS. 

For this demo, predictive motor maintenance data is being collected via bluetooth (BLE) from an [STEVAL-PROTEUS1 Industrial Evaluation Sensor](https://www.st.com/en/evaluation-tools/steval-proteus1.html). This data includes vibration speed, acceleration, and frequency data that can be used to monitor the health of field machines from anywhere with an internet connection.

<img src=".//media/image34.png"/> 

<img src=".//media/image33.png"/>

## Step 1: Make an IoTConnect Account
* To get started making an IoTConnect account, you can contact our team at info@iotconnect.io

## Step 2: Sign in to IoTConnect Account
* Navigate to https://awspoc.iotconnect.io/ and enter your account credentials.
   * This should bring you to your AWS IoTConnect Dashboard.

## Step 3: Import a Template for Your Device 
* Within this git repo, navigate to the PROTEUS_MP157F_Demo directory and click on the file called MP157F_template.JSON.

<img src=".//media/image31.png"/>

* Download the template file to your PC by clicking on the download button for the file, shown below.

<img src=".//media/image29.png"/>
  
* On the far-left side of the screen is a navy-blue toolbar, hover your cursor over the icon that looks like a processor chip and choose “Device” out of the dropdown options (shown below). 

<img src=".//media/image1.png"/>

* On the toolbar at the bottom of the page, select the “Templates” tab.

<img src=".//media/image2.png"/>

* On the Templates page, click the “Create Template” button in the top right corner of the screen. 

<img src=".//media/image3.png"/>

* In the upper-right area of the scree, click on the "Import" button.

<img src=".//media/image30.png"/>

* In the resulting pop-up window, click on the "Browse" button, navigate to where you have the template file downloaded, and select the template file. Click on the "Save" button afterwards.

<img src=".//media/image32.png"/>

## Step 4: Create a Your Device in IoTConnect
* Navigate back to the “Device” menu and click on “Create Device” in the top right corner of the screen.

<img src=".//media/image5.png"/>

* For the default configuration (no device naming configuration in final script), enter the following information and then click “Save and View”:
   * Unique Id: STM32MP157F
   * Display Name: STM32MP157F
   * Entity: Avnet
   * Template: MP157F
     
* For a custom UniqueID/DisplayName (device naming configuration in final script), enter the following information and then click “Save and View”:
   * Unique Id: <Your UniqueID/DisplayName Here>
   * Display Name: <Your UniqueID/DisplayName Here>
   * Entity: Avnet
   * Template: MP157F
 
      * **NOTE: This demo is deisgned for the Unique ID and the Display Name to be exactly the same, so it is critical that you make them identical to each other. It will not work otherwise.**
 
<img src=".//media/image6.png"/>

* In the resulting page, click “Connection Info” in the top-right corner of the page.

<img src=".//media/image7.png"/>

* Click on the yellow and green certificate icon in the top-right corner of the resulting pop-up to download the zipped certificate package called “ST32MP157F-certificates.”

<img src=".//media/image8.png"/>

* Extract the certificate package folder and copy the resulting certificates folder to a USB Storage Drive (flash drive). The folder should include:
   * pk_STM32MP157F.pem
   * cert_STM32MP157F.crt
 
**Do not rename the folder, it needs to keep the name “STM32MP157F-certificates” in order to work properly.**

## Step 5: PROTEUS Sensor Setup
* For assembly, follow section 4.1 in the provided [getting started document](https://www.st.com/resource/en/user_manual/um3000-getting-started-with-the-stevalproteus1-evaluation-kit-for-condition-monitoring-based-on-the-24-ghz-stm32wb5mmg-module-stmicroelectronics.pdf) for the PROTEUS. Getting the battery connector to solidly seat into its slot on the main board is a bit tricky, so make sure you take your time on that step.
  
* After the sensor kit is assembled, power the board with a Micro-USB cable. While the device has a battery, its level of charge when it comes from the manufacturer can vary.

* Using a small flathead screwdriver (the kind you might use to repair a set of eyeglasses), a straightened paperclip, or some type of small blunt pin, press and hold the S2 power switch down for 3 seconds. If you have the device sitting right-side-up on a desk with the Micro-USB connector facing to your left, the S2 button will be accessed through the only slot in the plastic casing that is facing you.

<img src=".//media/image35.png"/>

* At this point, your PROTEUS sensor kit is ready for use.

## Step 6: Flash IoTConnect-Compatible Image to STM32MP157F-DK2 Board
* To download the zipped image folder, [click here](https://saleshosted.z13.web.core.windows.net/sdk/st/stmp1/proteus/OSTL_6.1_IoTConnect_Compatible.zip).
* Unzip the folder to a known location.
* Download and Install the [STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html) software (the utility for flashing the image to the device).
   * You may have to create an ST account (it's free) to get access to the software download.
* Set up the STM32MP157F-DK board for flashing:
   * On the underside of the board, flip both of the large dipswitches (directly opposite of the HDMI port) to the "OFF" position.
  
      <img src=".//media/image16.png"/>
      
   * Power the board with a USB-C cable connected to the "PWR_IN" USB-C port connected to a 5VDC supply with at least 1.0A of output.
   
      <img src=".//media/image19.png"/>
      
   * Connect the USB-C "USB" port of your board to your PC with the included USB-C cable.
      * If your PC does not have a USB-C port, you may use a USB-A to USB-C cable and connect it to a normal USB-A port on your PC.
   
      <img src=".//media/image20.png"/>
   
   * Insert the included SD card into the SD card slot on the board.
      
   * Push the "RESET" button on your board to ensure it boots into flashing mode (the LCD display of the board should be black when it has booted into flashing mode).

<img src=".//media/image18.png"/>
      
* Run the STM32CubeProgrammer software and click on the "Open file" tab.

<img src=".//media/image21.png"/>
      
* Navigate to the directory where you have the unzipped "OpenSTLinux_IoTConnect_Compatible" folder, and then navigate through the folder to get to this directory: {Your preliminary directory}\OSTL_6.1_IoTConnect_Compatible\images\stm32mp1\flashlayout_st-image-weston\optee
   * Select the FlashLayout_sdcard_stm32mp157F-dk2-optee.tsv file and then click "Open." 
   
<img src=".//media/image22.png"/>
      
* Next, click on the "Browse" button to select the binaries path.
   
<img src=".//media/image23.png"/>
   
* Navigate once again to the directory where you have the unzipped "OpenSTLinux_IoTConnect_Compatible" folder, and then navigate through the folder to get to this directory: {Your preliminary directory}\OSTL_6.1_IoTConnect_Compatible\images\stm32mp1
   * Select the stm32mp1 folder and then click "Select folder."

<img src=".//media/image24.png"/>
      
* Back in the STM32CubeProgrammer window, on the right-hand side of the screen, if the "Port" is listed as "No DFU...," make sure your USB cable is connected both to your PC and the board, and then click the revolving arrows icon.

<img src=".//media/image25.png"/>
     
* When the device is recognized by the software, the port listing will be "USB" followed by a number, such as 1. The serial number of your board should also be listed beneath the port name.

<img src=".//media/image26.png"/>
    
* You are ready to flash. Click the "Download" button to begin the flashing process.
   * The STM32MP157F-DK2 will turn off and on several times throughout the flashing process. It is important to not unplug or disturb it during the process. Given the size of the image it will usually take **up to 45 minutes** to flash.
   * It is worth noting that the LCD screen on the board will turn on with some output text during the flash process, so do not be alarmed.

<img src=".//media/image27.png"/>
   
* When the flash has completed successfully, this pop-up in the STM32CubeProgrammer window will appear.

<img src=".//media/image28.png"/>
   
* Now, flip the large dipswitches on the underside of your board both to the "ON" position, and once again hit the reset button to properly boot the new image from the SD card.

<img src=".//media/image17.png"/>
   
* **For the first boot after flashing, the board takes a few minutes to turn on.**

* To complete the setup process:
   * Connect the ethernet port of your board to your internet router using an ethernet cable.
   * Connect a USB mouse and keyboard to the board using 2 of the 4 onboard USB ports.
   * Optionally, you may connect the board to an external monitor using the HMDI port. 

## Step 7: Gather Files and Set Up Software
* Open a terminal window and run these commands in this order:
   * ```su```
   * ```apt-get update```
   * ```apt-get upgrade -y```
   * ```dd if=/dev/zero of=/swapfile bs=1024 count=1048576```
      * **(This command takes a few minutes to execute)**
   * ```chmod 600 /swapfile```
   * ```mkswap /swapfile```
   * ```swapon /swapfile```
   * ```apt-get install unzip python3-pip -y```
   * ```pip3 install bleak```
      * **(This command takes several minutes to execute)** 
   * ```mkdir /home/weston/Demo```
   * ```cd /home/weston/Demo```
   * ```curl -OL https://github.com/avnet-iotconnect/iotc-python-examples/archive/refs/heads/main.zip```
   * ```unzip main.zip```
   * ```cd iotc-python-examples-main/PROTEUS_MP157F_Demo```
   * **ONLY IF NOT USING DEFAULT UNIQUEID/DISPLAYNAME**
     * Insert your custom UniqueID/DisplayName into the command below:
     * ```sed -i 's/STM32MP157F/<CustomUniqueIDDisplayName>/g' STM32MP157_setup.sh```
       * For example if my custom UniqueID/DisplayName was "TestDevice" the command would be:
         * ```sed -i 's/STM32MP157F/TestDevice/g' STM32MP157_setup.sh```
   * ```chmod +x STM32MP157_setup.sh```
   * ```./STM32MP157_setup.sh```
      * When prompted, insert your flash drive containing your device certificates into a USB port on the ST32MP157F-DK2. 
 
## Step 8: Run the Demo
* To actually start the demo, first navigate to the project sample directory with this command:

 ```cd iotconnect-python-sdk-v1.0/sample```

* Then run the program with this command, replacing the placeholder variables with your specific IoTConnect CPID, Environment, and UniqueID:

  * ```python3 STM32MP157F-DK2_PROTEUS_Demo.py -c "<CPID_Goes_Here>" -e "<Environment_Goes_Here>" -u "<UniqueID_Goes_Here>"```
   
     * If using the default UniqueID/DisplayName, the command will be:

       * ```python3 STM32MP157F-DK2_PROTEUS_Demo.py -c "<CPID_Goes_Here>" -e "<Environment_Goes_Here>"```

* For example if my CPID was ABCDEFGHIJKLMNOP123456789, my Environment was TechnologyLab, and my device's Unique ID was TestDevice, my command would be:

  * ```python3 STM32MP157F-DK2_PROTEUS_Demo.py -c "ABCDEFGHIJKLMNOP123456789" -e "TechnologyLab" -u "TestDevice"```

     * If using the default UniqueID/DisplayName, the command would be:

       * ```python3 STM32MP157F-DK2_PROTEUS_Demo.py -c "ABCDEFGHIJKLMNOP123456789" -e "TechnologyLab"```

* To find your CPID and Environment, navigate to your main IoTConnect dashboard page, hover your curson over the gear icon on the tollbar located on the far-left side of the page, and then click "Key Vault":

<img src=".//media/image9.png"/>

* Your CPID and Environment will be shown as in the image below:

<img src=".//media/image10.png"/>

## Step 9: View the Data
* Navigate back to the “Device” menu and select your device named "STM32MP157F" (or your custom Display Name if you did not use the default).
   * You should see that the entry in the "Device Status" column shows a green "CONNECTED" label.

<img src=".//media/image13.png"/>

* Next, in the vertical toolbar on the left side of the page, select "Live Data."

<img src=".//media/image14.png"/>

* To get a more human-friendly report of the live telemetry data, click on the "Tabular" tab.
   * This tab allows you to scroll vertically to view previous data entires, and horizontally to see each individual attribute.

<img src=".//media/image15.png"/>
