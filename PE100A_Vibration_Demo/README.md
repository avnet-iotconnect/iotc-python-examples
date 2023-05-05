# Asus PE100A Motor Monitor Demo (For IoTConnect on AWS)

## Step 1: Make an IoTConnect Account
* To get started making an IoTConnect account, you can contact our team at info@iotconnect.io

## Step 2: Sign in to IoTConnect Account
* Navigate to https://awspoc.iotconnect.io/ and enter your account credentials.
* This should bring you to your AWS IoTConnect Dashboard.

## Step 3: Create a Template for Your Device 
* On the far-left side of the screen is a navy-blue toolbar, hover your cursor over the icon that looks like a processor chip and choose “Device” out of the dropdown options (shown below). 

<img src=".//media/wfi32-iot-board.png"/>

* On the toolbar at the bottom of the page, select the “Templates” tab.

<img src=".//media/wfi32-iot-board.png"/>

* On the Templates page, click the “Create Template” button in the top right corner of the screen. 

<img src=".//media/wfi32-iot-board.png"/>

* Enter the following information into the Template creation page and click “Save”:
  * Template Code: PE100
  * Template Name: PE100_AWS_Demo
  * Authentication Type: Self Signed Certificate
  * Device Message Version: 2.1

* Click on the “Attributes” tab below the information you just entered.

<img src=".//media/wfi32-iot-board.png"/>

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
 
Enter the following information and click “Save”:
  * Local Name: *Attribute Name Exactly as Listed*
  * Data Type: DECIMAL
  * Other fields are optional and not used for this demo

