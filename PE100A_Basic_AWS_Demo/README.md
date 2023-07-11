# Asus PE100A Basic Demo (For IoTConnect on AWS)

This demo uses an [ASUS PE100A Intelligent Edge Computer](https://iot.asus.com/products/intelligent-edge-computer/PE100A/) to run an IoTConnect program to monitor precise telemetry data in real-time on the IoTConnect cloud platform using AWS. 

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
  * Template Code: PE100
  * Template Name: PE100_AWS_Demo
  * Authentication Type: Self Signed Certificate
  * Device Message Version: 2.1

* Next, click on the “Attributes” tab below the information you just entered.

<img src=".//media/image4.png"/>
 
* Enter the following information and click “Save”:
   * Local Name: Random_Integer
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
   * Unique Id: PE100Demo
   * Display Name: PE100_Demo
   * Entity: Avnet
   * Template: PE100_AWS_Demo
 
<img src=".//media/image6.png"/>

* In the resulting page, click “Connection Info” in the top-right corner of the page.

<img src=".//media/image7.png"/>

* Click on the yellow and green certificate icon in the top-right corner of the resulting pop-up to download the zipped certificate package called “PE100_Demo-certificates.”

<img src=".//media/image8.png"/>

* Extract the certificate package folder and copy the resulting certificates folder to a USB Storage Drive (flash drive). The folder should include:
   * pk_PE100_Demo.pem
   * cert_PE100_Demo.crt
 
**Do not rename the folder, it needs to keep the name “PE100_Demo-certificates” in order to work properly.**

## Step 5: Gather Files and Set Up Software
* Open a terminal window and run these commands in this order:
   * ```cd /home/asus```
   * ```mkdir PE100_Demo```
   * ```cd PE100_Demo```
   * ```git clone https://github.com/avnet-iotconnect/iotc-pov-engineering.git```
   * ```cd iotc-pov-engineering/PE100A_Basic_AWS_Demo```
   * ```chmod +x PE100_setup.sh```
   * ```./PE100_setup.sh```
      * When prompted, insert your flash drive containing your device certificates into a USB port on the PE100A.
      * **You may need to remove your mouse connection to free up a USB port for this.**

* At the end of the setup script, the device will automatically reboot so the network configuration can update. 
 
## Step 8: Run the Demo
* First, open a terminal instance and navigate to the project sample directory with this command:

 ```cd /home/asus/PE100_Demo/iotconnect-python-sdk-v1.0/sample```

* Then run the program with this command, replacing the placeholder variables with your specific IoTConnect CPID and Environment:

```python3 PE100_Basic_AWS_Demo.py -c "CPID_Goes_Here" -e "Environment_Goes_Here"```

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
