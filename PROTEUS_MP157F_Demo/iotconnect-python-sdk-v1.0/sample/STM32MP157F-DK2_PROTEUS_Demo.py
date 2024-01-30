import sys
import json
import time
import threading
import random
from iotconnect import IoTConnectSDK
from datetime import datetime
import os
import getopt
import proteus_AI_plugin
import proteus_standard_plugin
sys.path.append("/home/weston/PROTEUS_MP157F_Demo")
import config

# Get CPID, Environment, uniqueID, and proteus FW values from command-line options
cpid = config.cpid
env = config.env
UniqueId = config.unique_id
fw = config.proteus_fw_version
	
SId = ""
Sdk=None
interval = 5
directmethodlist={}
ACKdirect=[]
device_list=[]

SdkOptions={
	"certificate" : { 
		"SSLKeyPath"  : "/home/weston/Demo/" + UniqueId + "-certificates/pk_" + UniqueId + ".pem", 
		"SSLCertPath" : "/home/weston/Demo/" + UniqueId + "-certificates/cert_" + UniqueId + ".crt",
		"SSLCaPath"   : "/home/weston/Demo/PROTEUS_MP157F_Demo/iotconnect-python-sdk-v1.0/sample/aws_cert/root-CA.pem"
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

def DeviceCallback(msg):
    global Sdk
    print("\n--- Command Message Received in Firmware ---")
    print(json.dumps(msg))
    cmdType = None
    if msg != None and len(msg.items()) != 0:
        cmdType = msg["ct"] if "ct"in msg else None
    # Other Command
    if cmdType == 0:
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
	
def TwinUpdateCallback(msg):
    global Sdk
    if msg:
        print("--- Twin Message Received ---")
        print(json.dumps(msg))
        if ("desired" in msg) and ("reported" not in msg):
            for j in msg["desired"]:
                if ("version" not in j) and ("uniqueId" not in j):
                    Sdk.UpdateTwin(j,msg["desired"][j])

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

def DeviceChangeCallback(msg):
    print(msg)

def InitCallback(response):
    print(response)
    
def main():
    global SId,cpid,env,SdkOptions,Sdk,ACKdirect,device_list,fw
    try:
        with IoTConnectSDK(UniqueId,SId,cpid,env,SdkOptions,DeviceConectionCallback) as Sdk:
            try:
		if fw == "Standard":
		    proteus_thread = threading.Thread(target=proteus_standard_plugin.proteus_loop)
		else:
                    proteus_thread = threading.Thread(target=proteus_AI_plugin.proteus_loop)
                proteus_thread.start()
                Sdk.onDeviceCommand(DeviceCallback)
                Sdk.onTwinChangeCommand(TwinUpdateCallback)
                Sdk.onOTACommand(DeviceFirmwareCallback)
                Sdk.onDeviceChangeCommand(DeviceChangeCallback)
                Sdk.getTwins()
                device_list=Sdk.Getdevice()
                while True:
		    if fw == "Standard":
		        dObj = [{
			    "uniqueId": UniqueId,
			    "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
			    #Access updated data dictionary from plugin file
			    "data": proteus_standard_plugin.telemetry
		        }]
		    else:
                        dObj = [{
                            "uniqueId": UniqueId,
                            "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
			    #Access updated data dictionary from plugin file
                            "data": proteus_AI_plugin.telemetry
                        }]
                    sendBackToSDK(Sdk, dObj)
                    
            except KeyboardInterrupt:
                print ("Keyboard Interrupt Exception")
                sys.exit(0)
                 
    except Exception as ex:
        print(ex)
        sys.exit(0)

if __name__ == "__main__":
    main()
