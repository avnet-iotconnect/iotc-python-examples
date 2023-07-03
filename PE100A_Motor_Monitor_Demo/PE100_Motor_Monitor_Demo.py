import sys
import json
import time
import threading
import random
from iotconnect import IoTConnectSDK
from datetime import datetime
import os
import minimalmodbus
import getopt
import signal
from ModbusDevice import ModbusDevice
from ADAM import *

cpid = ""
env = ""

argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(argv,"c:e:")
except:
    print("Options error")
for opt, arg in opts:
    if opt == '-c':
        cpid = arg
    elif opt == '-e':
        env = arg
    else:
	raise Exception("Invalid option.")

PORT = '/dev/ttymxc1'

instrument = minimalmodbus.Instrument(PORT, 1, minimalmodbus.MODE_RTU)

instrument.serial.baudrate = 19200
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 1

instrument.close_port_after_each_call = True
instrument.clear_buffers_before_each_transaction = True

#Setting up connection to ADAM-6017 device
adam_ip="169.254.169.108"
adam_port=502
adam = None
adam = ADAM6017(adam_ip, adam_port)
if(adam.connect()==False):
    print("Error connecting to ip %s" % adam_ip)
if(adam.confirm_device()==False):
    print("ADAM-6017 device not valid!")
adam.write_channel_typecode(0,0x0180);


"""
* ## Prerequisite parameter to run this sampel code
* uniqueId     :: Its device ID which register on IotConnect platform and also its status has Active and Acquired
* cpId         :: It need to get from the IoTConnect platform "Settings->Key Vault". 
* env          :: It need to get from the IoTConnect platform "Settings->Key Vault". 
* SId 	       :: SId is the company code. You can get it from the IoTConnect UI portal "Settings -> Key Vault -> SDK Identities -> select language Python and Version 1.0"
* interval     :: send data frequency in seconds
* sdkOptions   :: It helps to define the path of self signed and CA signed certificate as well as define the offlinne storage configuration.
"""

UniqueId = "PE100Demo"
SId = ""

Sdk=None
interval = 5
directmethodlist={}
ACKdirect=[]
device_list=[]
"""
* sdkOptions is optional. Mandatory for "certificate" X.509 device authentication type
* "certificate" : It indicated to define the path of the certificate file. Mandatory for X.509/SSL device CA signed or self-signed authentication type only.
* 	- SSLKeyPath: your device key
* 	- SSLCertPath: your device certificate
* 	- SSLCaPath : Root CA certificate
* 	- Windows + Linux OS: Use "/" forward slash (Example: Windows: "E:/folder1/folder2/certificate", Linux: "/home/folder1/folder2/certificate")
* "offlineStorage" : Define the configuration related to the offline data storage 
* 	- disabled : false = offline data storing, true = not storing offline data 
* 	- availSpaceInMb : Define the file size of offline data which should be in (MB)
* 	- fileCount : Number of files need to create for offline data
* "devicePrimaryKey" : It is optional parameter. Mandatory for the Symmetric Key Authentication support only. It gets from the IoTConnect UI portal "Device -> Select device -> info(Tab) -> Connection Info -> Device Connection".
    - - "devicePrimaryKey": "<<your Key>>"
* Note: sdkOptions is optional but mandatory for SSL/x509 device authentication type only. Define proper setting or leave it NULL. If you not provide the offline storage it will set the default settings as per defined above. It may harm your device by storing the large data. Once memory get full may chance to stop the execution.
"""


SdkOptions={
	"certificate" : { 
		"SSLKeyPath"  : "/home/asus/PE100_Demo/pk_PE100_Demo.pem", 
		"SSLCertPath" : "/home/asus/PE100_Demo/cert_PE100_Demo.crt",
		"SSLCaPath"   : "/home/asus/PE100_Demo/root-CA.pem"
        
	},
    "offlineStorage":{
        "disabled": False,
	    "availSpaceInMb": 0.01,
	    "fileCount": 5,
        "keepalive":60
    },
    "skipValidation":False,
    "discoveryUrl":"https://awsdiscovery.iotconnect.io/",
    "IsDebug": False
   
}


"""
 * Type    : Callback Function "DeviceCallback()"
 * Usage   : Firmware will receive commands from cloud. You can manage your business logic as per received command.
 * Input   :  
 * Output  : Receive device command, firmware command and other device initialize error response 
"""

def DeviceCallback(msg):
    global Sdk
    print("\n--- Command Message Received in Firmware ---")
    print(json.dumps(msg))
    cmdType = None
    if msg != None and len(msg.items()) != 0:
        cmdType = msg["ct"] if "ct"in msg else None
    # Other Command
    if cmdType == 0:
        """
        * Type    : Public Method "sendAck()"
        * Usage   : Send device command received acknowledgment to cloud
        * 
        * - status Type
        *     st = 6; // Device command Ack status 
        *     st = 4; // Failed Ack
        * - Message Type
        *     msgType = 5; // for "0x01" device command 
        """
        data=msg
        if data != None:
            if "id" in data:
                if "ack" in data and data["ack"]:
                    Sdk.sendAckCmd(data["ack"],7,"sucessfull",data["id"])  #fail=4,executed= 5,sucess=7,6=executedack
            else:
                if "ack" in data and data["ack"]:
                    Sdk.sendAckCmd(data["ack"],7,"sucessfull") #fail=4,executed= 5,sucess=7,6=executedack
    else:
        print("rule command",msg)

    # Firmware Upgrade
def DeviceFirmwareCallback(msg):
    global Sdk,device_list
    print("\n--- firmware Command Message Received ---")
    print(json.dumps(msg))
    cmdType = None
    if msg != None and len(msg.items()) != 0:
        cmdType = msg["ct"] if msg["ct"] != None else None

    if cmdType == 1:
        """
        * Type    : Public Method "sendAck()"
        * Usage   : Send firmware command received acknowledgement to cloud
        * - status Type
        *     st = 7; // firmware OTA command Ack status 
        *     st = 4; // Failed Ack
        * - Message Type
        *     msgType = 11; // for "0x02" Firmware command
        """
        data = msg
        if data != None:
            if ("urls" in data) and data["urls"]:
                for url_list in data["urls"]:
                    if "tg" in url_list:
                        for i in device_list:
                            if "tg" in i and (i["tg"] == url_list["tg"]):
                                Sdk.sendOTAAckCmd(data["ack"],0,"sucessfull",i["id"]) #Success=0, Failed = 1, Executed/DownloadingInProgress=2, Executed/DownloadDone=3, Failed/DownloadFailed=4
                    else:
                        Sdk.sendOTAAckCmd(data["ack"],0,"sucessfull") #Success=0, Failed = 1, Executed/DownloadingInProgress=2, Executed/DownloadDone=3, Failed/DownloadFailed=4

def DeviceConectionCallback(msg):  
    cmdType = None
    if msg != None and len(msg.items()) != 0:
        cmdType = msg["ct"] if msg["ct"] != None else None
    #connection status
    if cmdType == 116:
        #Device connection status e.g. data["command"] = true(connected) or false(disconnected)
        print(json.dumps(msg))

"""
 * Type    : Public Method "UpdateTwin()"
 * Usage   : Update the twin reported property
 * Input   : Desired property "key" and Desired property "value"
 * Output  : 
"""

"""
 * Type    : Callback Function "TwinUpdateCallback()"
 * Usage   : Manage twin properties as per business logic to update the twin reported property
 * Input   : 
 * Output  : Receive twin Desired and twin Reported properties
"""
def TwinUpdateCallback(msg):
    global Sdk
    if msg:
        print("--- Twin Message Received ---")
        print(json.dumps(msg))
        if ("desired" in msg) and ("reported" not in msg):
            for j in msg["desired"]:
                if ("version" not in j) and ("uniqueId" not in j):
                    Sdk.UpdateTwin(j,msg["desired"][j])

"""
 * Type    : Public data Method "SendData()"
 * Usage   : To publish the data on cloud D2C 
 * Input   : Predefined data object 
 * Output  : 
"""
def sendBackToSDK(sdk, dataArray):
    sdk.SendData(dataArray)
    time.sleep(interval)

def DirectMethodCallback1(msg,methodname,rId):
    global Sdk,ACKdirect
    print(msg)
    print(methodname)
    print(rId)
    data={"data":"succed"}
    ACKdirect.append({"data":data,"status":200,"reqId":rId})

def DirectMethodCallback(msg,methodname,rId):
    global Sdk,ACKdirect
    print(msg)
    print(methodname)
    print(rId)
    data={"data":"fail"}
    ACKdirect.append({"data":data,"status":200,"reqId":rId})

def DeviceChangCallback(msg):
    print(msg)

def InitCallback(response):
    print(response)

def delete_child_callback(msg):
    print(msg)

def attributeDetails(data):
    print ("attribute received in firmware")
    print (data)
    



def main():
    global SId,cpid,env,SdkOptions,Sdk,ACKdirect,device_list
    
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
        with IoTConnectSDK(UniqueId,SId,cpid,env,SdkOptions,DeviceConectionCallback) as Sdk:
            try:
                """
                * Type    : Public Method "GetAllTwins()"
                * Usage   : Send request to get all the twin properties Desired and Reported
                * Input   : 
                * Output  : 
                """
                Sdk.onDeviceCommand(DeviceCallback)
                Sdk.onTwinChangeCommand(TwinUpdateCallback)
                Sdk.onOTACommand(DeviceFirmwareCallback)
                Sdk.onDeviceChangeCommand(DeviceChangCallback)
                Sdk.getTwins()
                device_list=Sdk.Getdevice()
                while True:
                    
                    data = {
                    "z_rms_velo_in_sec": instrument.read_register(2400,4),
                    "z_rms_velo_mm_sec": instrument.read_register(2402,3),
                    "temp_c": instrument.read_register(42,2),
                    "temp_f": instrument.read_register(48,2),
                    "x_rms_velo_in_sec": instrument.read_register(2450,4),
                    "x_rms_velo_mm_sec": instrument.read_register(2452,3),
                    "z_peak_accel_g": instrument.read_register(2406,3),
                    "x_peak_accel_g": instrument.read_register(2456,3),
                    "z_peak_velo_frq": instrument.read_register(2404,1),
                    "x_peak_velo_frq": instrument.read_register(2454,1),
                    "z_rms_accel_g": instrument.read_register(2405,3),
                    "x_rms_accel_g": instrument.read_register(2455,3),
                    "z_kurtosis": instrument.read_register(2408,3),
                    "x_kurtosis": instrument.read_register(2458,3),
                    "z_crest_fact": instrument.read_register(2407,3),
                    "x_crest_fact": instrument.read_register(2457,3),
                    "z_peak_velo_in_sec": instrument.read_register(2401,4),
                    "z_peak_velo_mm_sec": instrument.read_register(2403,3),
                    "x_peak_velo_in_sec": instrument.read_register(2451,4),
                    "x_peak_velo_mm_sec": instrument.read_register(2453,3),
                    "z_high_frq_rms_accel_g": instrument.read_register(2409,3),
                    "x_high_frq_rms_accel_g": instrument.read_register(2459,3),
                    "ac_current_amps": (adam.convert_uint(adam.read_channel(0), 4, 20) - 4)/8.0
                        }
                    dObj = [{
                        "uniqueId": UniqueId,
                        "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        "data": data
                    }]
                    
                    
                    """
                    * Add your device attributes and respective value here as per standard format defined in sdk documentation
                    * "time" : Date format should be as defined //"2021-01-24T10:06:17.857Z" 
                    * "data" : JSON data type format // {"temperature": 15.55, "gyroscope" : { 'x' : -1.2 }}
                    """
 
                    sendBackToSDK(Sdk, dObj)
                    
            except KeyboardInterrupt:
                print ("Keyboard Interrupt Exception")
                os.abort()
                
                
    except Exception as ex:
        print(ex)
        sys.exit(0)

if __name__ == "__main__":
    main()
