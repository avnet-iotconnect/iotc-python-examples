"""
  ******************************************************************************
  * @file   : iotconnect-sdk-1.0-firmware-python_msg-2_1.py
  * @author : Softweb Solutions An Avnet Company
  * @modify : 02-January-2023
  * @brief  : Firmware part for Python SDK 1.0
  ******************************************************************************
"""

"""
 * Hope you have installed the Python SDK v1.0 as guided in README.md file or from documentation portal.
 * Import the IoTConnect SDK package and other required packages
"""
import sys
import json
import time
import random
import keyboard  # Library to detect key presses
from iotconnect import IoTConnectSDK
from datetime import datetime
import os
import threading  # To handle the timer

UniqueId = "Your UniqueId"
Sdk = None
interval = 2
directmethodlist={}
ACKdirect=[]
current_temp_unit = "F"  # Default temperature unit

SdkOptions={
	"certificate" : { 
        "SSLKeyPath"  : "",    #aws=pk_devicename.pem   ||   #az=device.key
        "SSLCertPath" : "",    #aws=cert_devicename.crt ||   #az=device.pem
        "SSLCaPath"   : ""     #aws=root-CA.pem         ||   #az=rootCA.pem
    },
    "offlineStorage": {
        "disabled": False,
        "availSpaceInMb": 0.01,
        "fileCount": 5,
        "keepalive": 60
    },
    "skipValidation": False,
    "discoveryUrl": "https://awsdiscovery.iotconnect.io",
    "IsDebug": False,
    "cpid" : "Your CPID ",
    "sId" : "Your SID",
    "env" : "Your env",
    "pf"  : "Your pf"
}

health_values = {
    1: {"heartrate": 65, "spo2": 98, "temp_C": 36.6, "temp_F": 97.9, "indicator": "normal"},
    2: {"heartrate": 70, "spo2": 97, "temp_C": 36.8, "temp_F": 98.2, "indicator": "normal"},
    3: {"heartrate": 75, "spo2": 96, "temp_C": 37.0, "temp_F": 98.6, "indicator": "normal"},
    4: {"heartrate": 80, "spo2": 95, "temp_C": 37.2, "temp_F": 99.0, "indicator": "normal"},
    5: {"heartrate": 85, "spo2": 94, "temp_C": 37.7, "temp_F": 99.9, "indicator": "concern"},
    6: {"heartrate": 55, "spo2": 92, "temp_C": 37.8, "temp_F": 100.0, "indicator": "concern"},
    7: {"heartrate": 90, "spo2": 91, "temp_C": 38.0, "temp_F": 100.4, "indicator": "concern"},
    8: {"heartrate": 95, "spo2": 88, "temp_C": 38.5, "temp_F": 101.3, "indicator": "critical"},
    9: {"heartrate": 45, "spo2": 85, "temp_C": 39.0, "temp_F": 102.2, "indicator": "critical"},
    0: {"heartrate": 100, "spo2": 82, "temp_C": 39.5, "temp_F": 103.1, "indicator": "critical"}
}


def DeviceCallback(msg):
    global Sdk, current_temp_unit
    print("\n--- Command Message Received in Firmware ---")
    print(json.dumps(msg))
    cmdType = None
    if msg and len(msg.items()) != 0:
        cmdType = msg["ct"] if "ct" in msg else None
    # Handle commands
    if cmdType == 0:
        data = msg
        if data!= None:
            #print(data)
            if "cmd" in data and data["cmd"].startswith("temp_unit"):
                new_unit = data["cmd"].split()[-1]
                if new_unit in ["C", "F"]:
                    current_temp_unit = new_unit
                    print(f"Temperature unit changed to {current_temp_unit}")
            if "id" in data:
                if "ack" in data and data["ack"]:
                    Sdk.sendAckCmd(data["ack"], 7, "successful", data["id"])
            else:
                if "ack" in data and data["ack"]:
                    Sdk.sendAckCmd(data["ack"], 7, "successful")
    else:
        print("rule command", msg)


def TwinUpdateCallback(msg):
    global Sdk
    if msg:
        print("--- Twin Message Received ---")
        print(json.dumps(msg))
        if "desired" in msg and "reported" not in msg:
            for j in msg["desired"]:
                if "version" not in j and "uniqueId" not in j:
                    Sdk.UpdateTwin(j, msg["desired"][j])


def sendBackToSDK(sdk, dataArray):
    sdk.SendData(dataArray)


def reset_to_zero():
    global Sdk
    dObj = [{
        "uniqueId": UniqueId,
        "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "data": {
            "heartrate": 0,
            "spo2": 0,
            "temperature": 93,
            "temp_unit": current_temp_unit,
            "indicator": "N/A"                              
        }
    }]
    print("Resetting values to zero")
    sendBackToSDK(Sdk, dObj)
    print("Values reset to zero")


def on_key_press(event):
    global Sdk, current_temp_unit

    if event.name.isdigit():
        health_status = int(event.name)
        if health_status == 0:
            health_status = 0  # Ensure '0' key maps correctly to 0
        if 0 <= health_status <= 9:                      
            health_data = health_values[health_status]
            temp_value = health_data[f"temp_{current_temp_unit}"]

            dObj = [{
                "uniqueId": UniqueId,
                "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                "data": {
                    "heartrate": health_data["heartrate"],
                    "spo2": health_data["spo2"],
                    "temperature": temp_value,
                    "temp_unit": current_temp_unit,
                    "indicator": health_data["indicator"]
                }
            }]
            print(f"Sending data for health status {health_status}: {dObj}")
            sendBackToSDK(Sdk, dObj)
            print(f"Data for health status {health_status} sent successfully.")

            # Start timer to reset values after 5 seconds
            timer = threading.Timer(6.0, reset_to_zero)
            timer.start()


def main():
    global SdkOptions, Sdk, ACKdirect,device_list, current_temp_unit

    try:
        """
        if SdkOptions["certificate"]:
            for prop in SdkOptions["certificate"]:
                if os.path.isfile(SdkOptions["certificate"][prop]):
                    pass
                else:
                    print("please give proper path")
                    break
        else:
            print("you are not use auth type CA sign or self CA sign ") 
        """    
        """
        * Type    : Object Initialization "IoTConnectSDK()"
        * Usage   : To Initialize SDK and Device cinnection
        * Input   : cpId, uniqueId, sdkOptions, env as explained above and DeviceCallback and TwinUpdateCallback is callback functions
        * Output  : Callback methods for device command and twin properties
        """
        
        with IoTConnectSDK(UniqueId, SdkOptions, DeviceCallback) as Sdk:
            try:
                Sdk.onDeviceCommand(DeviceCallback)
                Sdk.onTwinChangeCommand(TwinUpdateCallback)
                Sdk.getTwins()

                # Setup key listener
                keyboard.on_press(on_key_press)

                # Keep the program running
                print("Press keys 0-9 to send health status data. Press ESC to exit.")
                keyboard.wait('esc')

            except KeyboardInterrupt:
                print("Keyboard Interrupt Exception")
                os.abort()

    except Exception as ex:
        sys.exit(0)


if __name__ == "__main__":
    main()
