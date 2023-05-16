## Softweb Solutions Inc
## IOT Connect SDK: Software Development Kit 3.0.1 

**Prerequisite tools:**

1. Python : Python version 2.7, 3.5 and 3.6
	-Note:- windows os only python 2.7.
2. pip : pip is compatible to the python version
3. setuptools : Required to install IOTConnect SDK

If you want to uninstall your older package:-
# make sure which pip you are use for install packege that you have to use for uninsall (pip,pip3)
    - pip list 
    - find your package
    - pip uninsall <<package name>>

**Installation:** 

1. Extract the "iotconnect-sdk-python-v3.0.1.zip"

2. To install the required libraries use the below command:
	Installation for python vesion 2.7:
		- Goto SDK directory path using terminal/Command prompt
		- cd iotconnect-sdk/
		- Extract the iotconnect-sdk-3.0.1.tar.gz
		- cd iotconnect-sdk-3.0.1
		- python setup.py install

	Installation for python vesion 3.5 and 3.6:
		- Goto SDK directory path using terminal/Command prompt
		- cd iotconnect-sdk/
		- pip3 install iotconnect-sdk-3.0.1.tar.gz


3. Using terminal/command prompt goto sample folder
	- cd sample 

4. You can take the firmware file from the above location and update the following details
	- Prerequisite input data as explained in the usage section as below #?
	- Update sensor attributes according to added in IoTConnect cloud platform.
	- If your device is secure then need to configure the x.509 certificate path such as given below in SDK Options otherwise leave it as it is.

5. Ready to go:
	- python python_sample.py
	
**Usage :**

Import library
```python
from iotconnect import IoTConnectSDK
```

- Prerequisite standard configuration data 
```python
uniqueId = <<uniqueId>>
cpid = <<CPID>> 
env = <<env>> // DEV, QA, POC, AVNETPOC, PROD(Default)
```
"uniqueId" 	: Your device uniqueId
"cpId" 		: It is the company code. It gets from the IoTConnect UI portal "Settings->Key Vault"
"env" 		: It is the UI platform environment. It gets from the IoTConnect UI portal "Settings->Key Vault"

- SdkOptions is for the SDK configuration and needs to parse in SDK object initialize call. You need to manage the below configuration as per your device authentication type.
```json
sdkOptions = {
    "certificate" : { //For SSL CA signed and SelfSigned authorized device only
        "SSLKeyPath"	: "<< SystemPath >>/device.key",
		"SSLCertPath"   : "<< SystemPath >>/device.pem",
		"SSLCaPath"     : "<< SystemPath >>/rootCA.pem"
	},
    "offlineStorage": { 
		"disabled": false, //default value = false, false = store data, true = not store data 
		"availSpaceInMb": 1, //size in MB, Default value = unlimted
		"fileCount": 5 // Default value = 1
	}
}
```
"certificate": It is indicated to define the path of the certificate file. Mandatory for X.509/SSL device CA signed or self-signed authentication type only.
	- SSLKeyPath: your device key
	- SSLCertPath: your device certificate
	- SSLCaPath : Root CA certificate
"offlineStorage" : Define the configuration related to the offline data storage 
	- disabled : false = offline data storing, true = not storing offline data 
	- availSpaceInMb : Define the file size of offline data which should be in (MB)
	- fileCount : Number of files need to create for offline data
"devicePrimaryKey": It is optional parameter. Mandatory for the Symmetric Key Authentication support only. It gets from the IoTConnect UI portal "Device -> Select device -> info(Tab) -> Connection Info -> Device Connection".
        -  "devicePrimaryKey": "<<your Key>>"
Note: sdkOptions is optional but mandatory for SSL/x509 device authentication type only. Define proper setting or leave it NULL. If you do not provide offline storage, it will set the default settings as per defined above. It may harm your device by storing the large data. Once memory gets full may chance to stop the execution.


- To initialize the SDK object need to import below sdk package
```python
IoTConnectSDK(cpId, uniqueId,scopeId ,DeviceCallback, TwinUpdateCallback,sdkOptions, env) as sdk:
```

- To receive the command from Cloud to Device(C2D).	
```python
	def DeviceCallback(msg):
		if(data["cmdType"] == "0x01")
			// Device Command
		elif(data["cmdType"] == "0x02")
			// Firmware Command
		elif(data["cmdType"] == "0x02")
			// Firmware Command
```

- To receive the twin from Cloud to Device(C2D).
```python
	def TwinUpdateCallback(msg):
		print(msg)
```
- To get the list of attributes with respective device.
```python
	sdk.GetAttributes();
```

- This is the standard data input format for Gateway and non Gateway device to send the data on IoTConnect cloud(D2C).
```json
	// For Non Gateway Device 
	data = [{
		"uniqueId": "<< Device UniqueId >>",
		"time" : "<< date >>",
		"data": {}
	}];

	// For Gateway and multiple child device 
	 data = [{
		"uniqueId": "<< Gateway Device UniqueId >>", // It should be must first object of the array
		"time": "<< date >>",
		"data": {}
	},
	{
		"uniqueId":"<< Child DeviceId >>", //Child device
		"time": "<< date >>",
		"data": {}
	}]
	sdk.SendData(data);
```
"time" : Date format should be as defined //"2021-01-24T10:06:17.857Z" 
"data" : JSON data type format // {"temperature": 15.55, "gyroscope" : { 'x' : -1.2 }}


- To send the command acknowledgment
```python
d2cMsg = {
	"ackId": data.ackId,
	"st": Acknowledgment status sent to cloud
	"msg": "", it is used to send your custom message
	"childId": "" it is use for gateway's child device OTA update
}
```
- ackId(*) : Command ack guid which is receive from command payload
- st(*) : Acknowledgment status sent to cloud (4 = Fail, 6 = Device command[0x01], 7 = Firmware OTA command[0x02])
- msg : Message 
- childId : 
	0x01 : null or "" for Device command  
	0x02 : null or "" for Gateway device and mandatory for Gateway child device's OTA udoate.
		   How to get the "childId" .?
		   - You will get child uniqueId for child device OTA command from payload "data.urls[~].uniqueId"
Note : (*) indicates the mandatory element of the object.

- Message Type
	```python
	msgType = 5; // for "0x01" device command 
	msgType = 11; // for "0x02" Firmware OTA command 
	sdk.SendAck(self,data,msgType) # msgType:- 11 and 5
	```
- To update the Twin Property
```python
	key = "<< Desired property key >>";
	value = "<< Desired Property value >>";
	sdk.UpdateTwin(key,value)
```
"key" 	:	Desired property key received from Twin callback message
"value"	:	Value of the respective desired property

- To disconnect the device from the cloud
```python
	sdk.Dispose()
```

- To get the all twin property Desired and Reported
```python
	sdk.GetAllTwins()
```

## Release Note :

** New Feature **
1. Offline data storage functionality with specific settings
2. Edge enable device support Gateway device too
3. Device and OTA command acknowledgment
4. It allows to disconnect the device client 
5. Introduce new methods:
	Dispose() : to disconnect the device
	GetAllTwins() : To receive all the twin properties
6. Support hard stop command to stop device client from cloud
7. Support OTA command with Gateway and child device
8. It allows sending the OTA command acknowledgment for Gateway and child device
9. Introduce new command(0x16) in device callback for Device connection status true(connected) or false(disconnected)

** Improvements **
1. We have updated the below methods name:
   To Initialize the SDK object:
	- Old : IoTConnectSDK(cpid, uniqueId, callbackMessage, twinCallbackMessage, env)
	- New : IoTConnectSDK(cpId, uniqueId,scopeId ,DeviceCallback, TwinUpdateCallback,sdkOptions, env)
   To send the data :
    - Old : SendData(data)
    - New : SendData(data)
   To update the Twin Reported Property :
    - New : UpdateTwin(key, value)
   To receive Device command callback :
    - Old : callbackMessage(data);
	- New : DeviceCallback(data);
   To receive OTA command callback :
    - Old : twinCallbackMessage(data);
	- New : TwinUpdateCallback(data);
2. Update the OTA command receiver payload for multiple OTA files
3. Use the "df" Data Frequency feature to control the flow of data which publish on cloud (For Non-Edge device only).