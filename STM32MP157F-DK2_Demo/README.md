# STM32MP157F-DK2 Demo (For IoTConnect on AWS)

This demo uses an [Discovery kit with STM32MP157F MPU](https://www.st.com/en/evaluation-tools/stm32mp157f-dk2.html) to run an IoTConnect program to monitor precise telemetry data in real-time on the IoTConnect cloud platform using AWS. 

For the purposes of this basic demo, the telemetry data is simple a random integer value, fittingly-dubbed "Random_Integer." More niche data coming from sensors and onboard measurements can be easily incorporated into the program as done with other Avnet IoT demos.

## Step 1: Make an IoTConnect Account
* To get started making an IoTConnect account, you can contact our team at info@iotconnect.io

## Step 2: Sign in to IoTConnect Account
* Navigate to https://awspoc.iotconnect.io/ and enter your account credentials.
   * This should bring you to your AWS IoTConnect Dashboard.

## Step 3: Create a Template for Your Device 
* On the far-left side of the screen is a navy-blue toolbar, hover your cursor over the icon that looks like a processor chip and choose “Device” out of the dropdown options (shown below). 

<img src=".//media/image1.png"/>

* On the toolbar at the bottom of the page, select the “Templates” tab.

<img src=".//media/image2.png"/>

* On the Templates page, click the “Create Template” button in the top right corner of the screen. 

<img src=".//media/image3.png"/>

* Enter the following information into the Template creation page and click “Save”:
  * Template Code: MP157F
  * Template Name: MP157F
  * Authentication Type: Self Signed Certificate
  * Device Message Version: 2.1

* Next, click on the “Attributes” tab below the information you just entered.

<img src=".//media/image4.png"/>

* For each of these attributes:
  * Random_Integer
 
* Enter the following information and click “Save”:
   * Local Name: ***Attribute Name Exactly as Listed***
   * Data Type: INTEGER
   * *Other fields are optional and not used for this demo*

* Then, click on the "Properties" tab.

<img src=".//media/image11.png"/>

* Update the Data Frequency to 5 seconds, and click save.

<img src=".//media/image12.png"/>

## Step 4: Create a Your Device in IoTConnect
* Navigate back to the “Device” menu and click on “Create Device” in the top right corner of the screen.

<img src=".//media/image5.png"/>

* Enter the following information and then click “Save and View”:
   * Unique Id: STM32MP157F
   * Display Name: STM32MP157F
   * Entity: Avnet
   * Template: MP157F
 
<img src=".//media/image6.png"/>

* In the resulting page, click “Connection Info” in the top-right corner of the page.

<img src=".//media/image7.png"/>

* Click on the yellow and green certificate icon in the top-right corner of the resulting pop-up to download the zipped certificate package called “ST32MP157F-certificates.”

<img src=".//media/image8.png"/>

* Extract the certificate package folder and copy the resulting certificates folder to a USB Storage Drive (flash drive). The folder should include:
   * pk_STM32MP157F.pem
   * cert_STM32MP157F.crt
 
**Do not rename the folder, it needs to keep the name “STM32MP157F-certificates” in order to work properly.**

## Step 5: Flash IoTConnect-Compatible Image to Board
* To download the zipped image folder, [click here](https://github.com/avnet-iotconnect/iotc-pov-engineering/raw/main/STM32MP157F-DK2_Demo/OpenSTLinux_IoTConnect_Compatible.zip).
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
      
* Navigate to the directory where you have the unzipped "OpenSTLinux_IoTConnect_Compatible" folder, and then navigate through the folder to get to this directory: {Your preliminary directory}\OpenSTLinux_IoTConnect_Compatible\images\stm32mp1\flashlayout_st-image-weston\optee
   * Select the FlashLayout_sdcard_stm32mp157c-dk2-optee.tsv file and then click "Open." 
      * The "...157f..." version of the file has issues so we have been instructed by ST to use the "...157c..." version.
   
<img src=".//media/image22.png"/>
      
* Next, click on the "Browse" button to select the binaries path.
   
<img src=".//media/image23.png"/>
   
* Navigate once again to the directory where you have the unzipped "OpenSTLinux_IoTConnect_Compatible" folder, and then navigate through the folder to get to this directory: {Your preliminary directory}\OpenSTLinux_IoTConnect_Compatible\images\stm32mp1
   * Select the stm32mp1 folder and then click "Select folder."

<img src=".//media/image24.png"/>
      
* Back in the STM32CubeProgrammer window, on the right-hand side of the screen, if the "Port" is listed as "No DFU...," make sure your USB cable is connected both to your PC and the board, and then click the revolving arrows icon.

<img src=".//media/image25.png"/>
     
* When the device is recognized by the software, the port listing will be "USB" followed by a number, such as 1. The serial number of your board should also be listed beneath the port name.

<img src=".//media/image26.png"/>
    
* You are ready to flash. Click the "Download" button to begin the flashing process.
   * The STM32MP157F-DK2 will turn off and on several times throughout the flashing process. It is important to not unplug or disturb it during the process. Given the size of the image it will usually take **between 30 and 45 minutes** to flash.
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

## Step 6: Gather Files and Set Up Software
* Open a terminal window and run these commands in this order:
   * ```su```
   * ```apt-get update```
   * ```apt-get upgrade -y```
   * ```apt-get install unzip python3-pip -y```
   * ```mkdir /home/weston/Demo```
   * ```cd /home/weston/Demo```
   * ```curl -OL https://github.com/avnet-iotconnect/iotc-pov-engineering/archive/refs/heads/main.zip```
   * ```unzip main.zip```
   * ```cd iotc-pov-engineering-main/STM32MP157F-DK2_Demo```
   * ```chmod +x STM32MP157_setup.sh```
   * ```./STM32MP157_setup.sh```
      * When prompted, insert your flash drive containing your device certificates into a USB port on the ST32MP157F-DK2. 
 
## Step 7: Run the Demo
* To actually start the demo, first navigate to the project sample directory with this command:

 ```cd /home/weston/Demo/iotc-pov-engineering-main/STM32MP157F-DK2_Demo/iotconnect-python-sdk-v1.0/sample```

* Then run the program with this command, replacing the placeholder variables with your specific IoTConnect CPID and Environment:

```python3 PE100_Motor_Monitor_Demo.py -c "CPID_Goes_Here" -e "Environment_Goes_Here"```

* For example if my CPID was ABCDEFGHIJKLMNOP123456789 and my Environment was TechnologyLab, my command would be:

```python3 STM32MP157F-DK2_Demo.py -c "ABCDEFGHIJKLMNOP123456789" -e "TechnologyLab"```

* To find your CPID and Environment, navigate to your main IoTConnect dashboard page, hover your curson over the gear icon on the tollbar located on the far-left side of the page, and then click "Key Vault":

<img src=".//media/image9.png"/>

* Your CPID and Environment will be shown as in the image below:

<img src=".//media/image10.png"/>

## Step 8: View the Data
* Navigate back to the “Device” menu and select your device named "STM32MP157F."
   * You should see that the entry in the "Device Status" column shows a green "CONNECTED" label.

<img src=".//media/image13.png"/>

* Next, in the vertical toolbar on the left side of the page, select "Live Data."

<img src=".//media/image14.png"/>

* To get a more human-friendly report of the live telemetry data, click on the "Tabular" tab.
   * This tab allows you to scroll vertically to view previous data entires, and horizontally to see each individual attribute.

<img src=".//media/image15.png"/>
