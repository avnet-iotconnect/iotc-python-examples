import sys
import json
import time
import threading
import random
from iotconnect import IoTConnectSDK
from datetime import datetime
import os

UniqueId = "PE100Demo" 
SId = "NTg0YWY3MzAyODU0NGE3NzhmM2JjYTE2OTY0MDFlMDg=UDE6MDM6MzUuMzk="

Sdk=None
interval = 60
directmethodlist={}
ACKdirect=[]
device_list=[]

SdkOptions={
	"certificate" : { 
		"SSLKeyPath"  : "/home/asus/PE100_Demo/PE100_Demo-certificates/pk_PE100_Demo.pem", 
		"SSLCertPath" : "/home/asus/PE100_Demo/PE100_Demo-certificates/cert_PE100_Demo.crt",
		"SSLCaPath"   : "/home/asus/PE100_Demo/root-CA.pem"
        
	},
    "offlineStorage":{
        "disabled": False,
	    "availSpaceInMb": 0.01,
	    "fileCount": 5,
        "keepalive":60
    },
    "skipValidation":False,
    # "devicePrimaryKey":"<<DevicePrimaryKey>>",
	# As per your Environment(Azure or Azure EU or AWS) uncomment single URL and commnet("#") rest of URLs.
    # "discoveryUrl":"https://eudiscovery.iotconnect.io" #Azure EU environment 
    # "discoveryUrl":"https://discovery.iotconnect.io", #Azure All Environment 
    "discoveryUrl":"http://52.204.155.38:219", #AWS pre-QA Environment
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
            #print(data)
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
    #return data,200,rId
    ACKdirect.append({"data":data,"status":200,"reqId":rId})
    #Sdk.DirectMethodACK(data,200,rId)

def DirectMethodCallback(msg,methodname,rId):
    global Sdk,ACKdirect
    print(msg)
    print(methodname)
    print(rId)
    data={"data":"fail"}
    #return data,200,rId
    ACKdirect.append({"data":data,"status":200,"reqId":rId})
    #Sdk.DirectMethodACK(data,200,rId)

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
    global SId,SdkOptions,Sdk,ACKdirect,device_list
    
    try:

        with IoTConnectSDK(UniqueId,SId,SdkOptions,DeviceConectionCallback) as Sdk:
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
                    data = {"Random_Integer": random.randint(1,100)}
                    dObj = [{
                        "uniqueId": UniqueId,
                        "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        "data": data
                    }]
                    sendBackToSDK(Sdk, dObj)
                    
            except KeyboardInterrupt:
                print ("Keyboard Interrupt Exception")
                os.abort()
                
                
    except Exception as ex:
        print(ex)
        sys.exit(0)

if __name__ == "__main__":
    main()
