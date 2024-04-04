import asyncio
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
import time
import sys
import pexpect
import importlib
sys.path.append("/home/weston/STM32MP157F_Demo")
import 

# Anomaly Detection mode can either be "Learning" or "Detection"
AD_Mode = "Learning"
# Anomaly Detection can be either be "On" or "Off"
AD_OnOff = "Off"
# Knowledge Reset button is either "Normal" or "Pressed"
Knowledge_Reset_Button = "Normal"

#This dictionary is what the main loop of the main 
#program will periodcially send as telemetry to IoTConnect
telemetry = {
    "NEAI_phase":"Not yet specified",
    "NEAI_state":"Not yet specified",
    "NEAI_progress_percentage":0,
    "NEAI_status":"Not yet specified",
    "NEAI_similarity_percentage":0
}


#This function resets the bluetooth system to make 
#sure that no devices are connected at the start of the program
def setup_bluetooth():
    setup_process = pexpect.spawn('bluetoothctl', encoding='utf-8')
    setup_process.expect('#')
    setup_process.sendline('power off')
    time.sleep(1)
    setup_process.sendline('power on')
    time.sleep(1)
    setup_process.close()


#This loop is what the dedicated proteus thread will run when started in the main loop
def main_loop():
    setup_bluetooth()
    #KICK OFF ST EXAMPLE
    while True:
        #CHECK EVERY HALF SECOND IF THERE IS NEW DATA IN THE QUEUE AND UPDATE THE DICTIONARY ACCORDINGLY
