# Asus PE100A Motor Monitor Demo (For IoTConnect on AWS)

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
  * Template Code: PE100
  * Template Name: PE100_AWS_Demo
  * Authentication Type: Self Signed Certificate
  * Device Message Version: 2.1

* Click on the “Attributes” tab below the information you just entered.

<img src=".//media/image4.png"/>

* For each of these attributes:
  * z_rms_velo_in_sec
  * z_rms_velo_mm_sec
  * temp_c
  * temp_f
  * x_rms_velo_in_sec
  * x_rms_velo_mm_sec
  * z_peak_accel_g
  * x_peak_accel_g
  * z_peak_velo_frq
  * x_peak_velo_frq
  * z_rms_accel_g
  * x_rms_accel_g
  * z_kurtosis
  * x_kurtosis
  * z_crest_fact
  * x_crest_fact
  * z_peak_velo_in_sec
  * z_peak_velo_mm_sec
  * x_peak_velo_in_sec
  * x_peak_velo_mm_sec
  * z_high_frq_rms_accel_g
  * x_high_frq_rms_accel_g
  * ac_current_amps
 
* Enter the following information and click “Save”:
   * Local Name: ***Attribute Name Exactly as Listed***
   * Data Type: DECIMAL
   * *Other fields are optional and not used for this demo*

## Step 4: Create a Your Device in IoTConnect
* Navigate back to the “Device” menu and click on “Create Device” in the top right corner of the screen.

<img src=".//media/image5.png"/>

* Enter the following information and then click “Save and View”:
   * Unique Id: PE100Demo
   * Display Name: PE100_Demo
   * Entity: Avnet
   * Template: PE100_AWS_Demo
 
<img src=".//media/image6.png"/>

* In the resulting page, click “Connection Info” in the top-right corner of the page.

<img src=".//media/image7.png"/>

* Click on the yellow and green certificate icon in the top-right corner of the resulting pop-up to download the zipped certificate package called “PE100_Demo-certificates.”

<img src=".//media/image8.png"/>

* Extract the certificate package folder and copy the individual files to a USB Storage Drive (flash drive). The files should include:
   * pk_PE100_Demo.pem
   * cert_PE100_Demo.crt
 
**Do not create a folder on the flash drive for these files, they need to be in the outer-most directory of the drive itself.**

## Step 5: Change UART to RS-485 
* Change the UART protocol to RS-485 by following section 3.3 of the [PE100A Software Manual](https://github.com/ASUS-IPC/ASUS-IPC/wiki/PE100A)
   * **Make sure to reboot the device after this is complete.**

## Step 6: Physically Set Up Demo Hardware
* Follow the diagram below to guide the physical setup of the demo:

<img src=".//media/PE100A_Motor_Monitor_Demo_Diagram.png"/>

* Within this "media" folder of this directory, there is a copy of the diagram (called “PE100A_Motor_Monitor_Demo_Diagram.png”) that can be downloaded for further inspection.

## Step 7: IoTConnect Python SDK
* Open a terminal window and run these commands in this order:
   * ```cd /home/asus```
   * ```mkdir PE100_Demo```
   * ```git clone https://github.com/avnet-iotconnect/iotc-pov-engineering.git```
   * ```cd iotc-pov-engineering```
   * ```chmod +x PE100_setup.sh```
   * ```./PE100_setup.sh```
      * When prompted, insert your flash drive containing your device certificates into a USB port on the PE100A.
      * **You may need to remove your mouse connection to free up a USB port for this.**
 
## Step 8: Run the Demo
* Run this command with your IoTConnect CPID and Environment instead of the placeholders:

```python3 PE100_Motor_Monitor_Demo.py -c "CPID_Goes_Here" -e "Environment_Goes_Here"```

   * For example if my CPID was ABCDEFGHIJKLMNOP123456789 and my Environment was TechnologyLab, my command would be:
      * ```python3 PE100_Motor_Monitor_Demo.py -c "ABCDEFGHIJKLMNOP123456789" -e "TechnologyLab"```



