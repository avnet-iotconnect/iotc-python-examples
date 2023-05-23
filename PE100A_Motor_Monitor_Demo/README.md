# Asus PE100A Motor Monitor Demo (For IoTConnect on AWS)

This demo uses an [ASUS PE100A Intelligent Edge Computer](https://iot.asus.com/products/intelligent-edge-computer/PE100A/) to run an IoTConnect program to monitor motor vibration and temperature with a [Banner QM30VT2-SS-9M Vibration and Temperature Sensor](https://www.bannerengineering.com/us/en/products/part.806274.html) as well as AC current-draw with an [Automation Direct ACTR005-42L-F Current Sensor](https://www.automationdirect.com/adc/shopping/catalog/sensors_-z-_encoders/current_-a-_voltage_sensors_(ac_-a-_dc)/1-phase_ac_current_transducers/actr005-42l-f). Telemetry data is sent to the online IoTConnect cloud platform using AWS and can be viewed in real-time for precise and continuous observation. 

For the purposes of reliably showcasing a broad range of motor health states, instead of a conventional electric motor the sensors are monitoring an [electromagnetic vibration plate](https://www.amazon.com/dp/B08CZ8BSMG?ref=ppx_yo2ov_dt_b_product_details&th=1) that has adjustable vibration amplitude which also causes higher current-draw and temperatures. To observe more extreme temperature changes with this demo, external heating or cooling sources can easily be introduced.

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

* Next, click on the “Attributes” tab below the information you just entered.

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

* Then, click on the "Properties" tab.

<img src=".//media/image11.png"/>

* Update the Data Frequency to 5 seconds, and click save.

<img src=".//media/image12.png"/>

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
   * *Note: You will have to open the PE100A and flip some dipswitches during this process*
   * **Make sure to reboot the device after this is complete.**

## Step 6: Physically Set Up Demo Hardware
* Follow the diagram below to guide the physical setup of the demo:

<img src=".//media/PE100A_Motor_Monitor_Demo_Diagram.png"/>

* Within this "media" folder of this directory, there is a copy of the diagram (called “PE100A_Motor_Monitor_Demo_Diagram.png”) that can be downloaded for further inspection.

## Step 7: Gather Files and Set Up Software
* Open a terminal window and run these commands in this order:
   * ```cd /home/asus```
   * ```mkdir PE100_Demo```
   * ```cd PE100_Demo```
   * ```git clone https://github.com/avnet-iotconnect/iotc-pov-engineering.git```
   * ```cd iotc-pov-engineering/PE100A_Motor_Monitor_Demo```
   * ```chmod +x PE100_setup.sh```
   * ```./PE100_setup.sh```
      * When prompted, insert your flash drive containing your device certificates into a USB port on the PE100A.
      * **You may need to remove your mouse connection to free up a USB port for this.**

* At the end of the setup script, the device will automatically reboot so the network configuration can update. 
 
## Step 8: Run the Demo
* First, open a terminal instance and navigate to the project sample directory with this command:

 ```cd /home/asus/PE100_Demo/iotconnect-python-sdk-v1.0/sample```

* Then run the program with this command, replacing the placeholder variables with your specific IoTConnect CPID and Environment:

```python3 PE100_Motor_Monitor_Demo.py -c "CPID_Goes_Here" -e "Environment_Goes_Here"```

* For example if my CPID was ABCDEFGHIJKLMNOP123456789 and my Environment was TechnologyLab, my command would be:
   * ```python3 PE100_Motor_Monitor_Demo.py -c "ABCDEFGHIJKLMNOP123456789" -e "TechnologyLab"```

* To find your CPID and Environment, navigate to your main IoTConnect dashboard page, hover your curson over the gear icon on the tollbar located on the far-left side of the page, and then click "Key Vault":

<img src=".//media/image9.png"/>

* Your CPID and Environment will be shown as in the image below:

<img src=".//media/image10.png"/>

## Step 9: View the Data
* Navigate back to the “Device” menu and select your device named "PE100Demo."
   * You should see that the entry in the "Device Status" column shows a green "CONNECTED" label.

<img src=".//media/image13.png"/>

* Next, in the vertical toolbar on the left side of the page, select "Live Data."

<img src=".//media/image14.png"/>

* To get a more human-friendly report of the live telemetry data, click on the "Tabular" tab.
   * This tab allows you to scroll vertically to view previous data entires, and horizontally to see each individual attribute.

<img src=".//media/image15.png"/>
