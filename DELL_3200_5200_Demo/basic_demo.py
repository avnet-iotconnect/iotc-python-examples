import json
import time
import random
from datetime import datetime
import os
import random

from iotconnect import IoTConnectSDK

# Get CPID, Environment, and uniqueID values from command-line options
with open("config.json") as f:
    config = json.load(f)

for key in ["sdk_id", "cpid", "env", "unique_id", "display_name"]:
    if not config[key]:
        raise ValueError(f"{key} in config.json cannot be empty. Please updated the config.json file")
    
for cert in [f"pk_{config['display_name']}.pem", f"cert_{config['display_name']}.crt", "root-CA.pem"]:
    if not os.path.exists(f"certificates/{cert}"):
        raise Exception(f"Missing cert file: {cert}")
	
interval = 5
directmethodlist={}
ACKdirect=[]
device_list=[]

SdkOptions={
	"certificate" : { 
		"SSLKeyPath"  : os.path.abspath(f"certificates/pk_{config['display_name']}.pem"),
		"SSLCertPath" : os.path.abspath(f"certificates/cert_{config['display_name']}.crt"),
		"SSLCaPath"   : os.path.abspath(f"certificates/root-CA.pem"),
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

def main():
    with IoTConnectSDK(config["unique_id"], config['sdk_id'], SdkOptions) as Sdk:
        try:
            while True:
                dObj = [{
                    "uniqueId": config["unique_id"],
                    "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                    #Access updated data dictionary from plugin file
                    "data": {"data": random.gauss(1, 0.1)}
                }]
                Sdk.SendData(dObj)
                time.sleep(interval)
        except KeyboardInterrupt:
            print ("Keyboard Interrupt Exception")


if __name__ == "__main__":
    main()