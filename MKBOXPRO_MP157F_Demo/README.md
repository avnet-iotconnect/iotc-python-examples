# MKBOXPRO / STM32MP157F-DK2 Demo (For IoTConnect on AWS)

This demo uses an [Discovery kit with STM32MP157F MPU](https://www.st.com/en/evaluation-tools/stm32mp157f-dk2.html) to run an IoTConnect program to monitor precise telemetry data in real-time on the IoTConnect cloud platform using AWS. 

For this demo, various types of sensor data is being collected via bluetooth (BLE) from an [SensorTile.box PRO](https://www.st.com/en/evaluation-tools/steval-mkboxpro.html). This data includes readinsg from temperature, air pressure, acceleration, gyroscope, magnetometer, and battery sensors.

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
   * Entity: (Any Generic Entity Will Work)
   * Template: MP157F
     
* For a custom UniqueID/DisplayName (device naming configuration in final script), enter the following information and then click “Save and View”:
   * Unique Id: <Your UniqueID/DisplayName Here>
   * Display Name: <Your UniqueID/DisplayName Here>
   * Entity: (Any Generic Entity Will Work)
   * Template: MP157F
 
      * **NOTE: For setup simplicity, this demo is deisgned for the Unique ID and the Display Name to be exactly the same, so it is critical that you make them identical to each other. It will not work otherwise.**
 
<img src=".//media/image6.png"/>

* In the resulting page, click “Connection Info” in the top-right corner of the page.

<img src=".//media/image7.png"/>

* Click on the yellow and green certificate icon in the top-right corner of the resulting pop-up to download the zipped certificate package.

<img src=".//media/image8.png"/>

* Extract the certificate package folder and save the resulting certificates folder to a known location. You will relocate them later into the setup.

## Step 5: MKBOXPRO Sensor Setup
* Power your MKBOXPRO Sensor pack with 5VDC using a USB-C cable.
* To ensure that your MKBOXPRO is running the firmware compatible with this demo, you will need to download and use the ST BLE Senor Classic mobile app (available on Android and iOS)
  * **NOTE: Make sure you download the "Classic" version of the app. There is a version just called "ST BLE Sensor" which is not compatible with this demo.**
* Turn on Bluetooth on your mobile device, and open the ST BLE Sensor Classic app.
* On the home page, click on the "Connect to a device" icon and then you should see your MKBOXPRO show up as the app scans for ST BLE devices, like this:

  <img src=".//media/stble_1.png"/>

* Click on your device, and then in the resulting screen, select the 3 dots in the lower-right corner of your screen

  <img src=".//media/stble_2.png"/>

* On the resulting screen, select "Board Configuration"

<img src=".//media/stble_3.png"/>

* Next, scroll down and select "Firmware Download"

<img src=".//media/stble_4.png"/>

* In the resulting screen, select the downward-pointing chevron to the right of the text "Not Selected"

<img src=".//media/stble_5.png"/>

* Now select the firmware pack called "FP-SNS-STBOX1_BLESensors v1.5.0"

<img src=".//media/stble_6.png"/>

* Now select "Swap to this Bank"

<img src=".//media/stble_7.png"/>

* You will be taken back to the Board Configuration menu. Select "Firmware Swap"

<img src=".//media/stble_8.png"/>

* The MKBOXPRO will boot up with the new firmware pack after the current Bluetooth connection is terminated, so close out of the ST BLE Sensor Classic app to do this.

* Your MKBOXPRO should now be ready for the demo.

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
   * Connect your board to the internet by either using an ethernet cable, or by following the optional Wi-Fi configuration step below.
   * You will also need to connect the STM32MP157 Discovery kit to your PC using a USB-A to micro-USB cable. Connect to the assigned COM Port using serial console application, such as [Tera Term](https://ttssh2.osdn.jp/index.html.en), or a browser application like [Google Chrome Labs Serial Terminal](https://googlechromelabs.github.io/serial-terminal/). Optionally, you may connect the board to an external monitor using the HMDI port and a keyboard/mouse.

## Step 7: Prepare Necessary Files
* In another browser tab, navigate to [the top of this repository] (https://github.com/avnet-iotconnect/iotc-python-examples/tree/main) and download the repository's zip file as shown here:

<img src=".//media/image_a.png"/>

* Unzip the downloaded folder and then open it.
  
* Navigate to the *iotc-python-examples-main* directory (the name of the overall repo and the first sub-directory will have the same name)
  
* Copy the *MKBOXPRO_MP157F_Demo* folder to a flash drive. This is the only part of the repository you will need for this demo.

* In the *MKBOXPRO_MP157F_Demo* directory on your flash drive, navigate to the *device_certificates* folder.

* Copy your two individual device certificates from the folder you saved in Step 4 into this folder. **You cannot copy the whole certificate folder, you must copy the individual *.pem* and *.crt* files.**

* Back in the *MKBOXPRO_MP157F_Demo* directory, open up the file *config.py* in a generic text editor.

* To find your CPID and Environment, navigate to your main IoTConnect dashboard page, hover your curson over the gear icon on the tollbar located on the far-left side of the page, and then click "Key Vault":

<img src=".//media/image9.png"/>

* Your CPID and Environment will be shown as in the image below:

<img src=".//media/image10.png"/>

* Copy your CPID and Environment into the *cpid* and *env* fields of *config.py*, **within the quotation marks.**

* Enter the Unique ID for your device from Step 4 into the *unique_id* field, **within the quotation marks.**

* Save the *config.py* file and close the text editor.

* Now remove the flash drive from your PC and insert it into a USB port on the STM32MP157F-DK2 gateway.

 
## Step 8: Configure the Gateway
* These steps can be completed using the serial terminal connected to the ST Discovery board, or using the weston terminal directly on the gateway.

* First, get admin privileges by entering this command:
  * ```su```

* Create a directory for the flash drive to mount to with this command:
  * ```mkdir /media/usbdrive```

* Now, mount the flash drive using this command:
  * ```mount /dev/sda1 /media/usbdrive```
    * If that command fails (will only fail if you have plugged/unplugged the flash drive from the gateway more than once), use this longer command instead:
      * ```mount /dev/sdb1 /media/usbdrive || mount /dev/sdc1 /media/usbdrive || mount /dev/sdd1 /media/usbdrive```

* **Wi-Fi Configuration (OPTIONAL)**
* To connect the gateway to the wireless network, execute this command:
  * ```/media/usbdrive/MKBOXPRO_MP157F_Demo/Wifi_Setup.sh```
    * NOTE: You will be asked to enter your network SSID and password during this script, as well as if it is your first time connecting the gateway to Wi-Fi
      * If you have already connected the gateway to Wi-Fi before and need to change the SSID or password, simply run the script again and answer **Y** to the first prompt
 

## Step 9: View the Data
* Navigate back to the “Device” menu and select your device named "STM32MP157F" (or your custom Display Name if you did not use the default).
   * You should see that the entry in the "Device Status" column shows a green "CONNECTED" label.

<img src=".//media/image13.png"/>

* Next, in the vertical toolbar on the left side of the page, select "Live Data."

<img src=".//media/image14.png"/>

* To get a more human-friendly report of the live telemetry data, click on the "Tabular" tab.
   * This tab allows you to scroll vertically to view previous data entires, and horizontally to see each individual attribute.

<img src=".//media/image15.png"/>
