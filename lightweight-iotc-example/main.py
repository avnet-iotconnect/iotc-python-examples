import sys
import os
import signal
import time
import getopt
from pathlib import Path
import syslog
import random

from iotconnect import IoTConnectSDK
from datetime import datetime

# These are Avnet libraries
import lib_config as config

# Only 1 global! Used to handle ctrl-c and control of
# program execution
g_running = True


''' Helper functions '''
def signal_handler(sig, frame):
    global g_running
    # Catch ctrl-c so we can shutdown gracefully
    if(sig==signal.SIGINT):
        log(" <--- catch ctrl-c")
    elif(sig==signal.SIGTERM):
        log(" --- Got SIGTERM")
    else:
        log(" --- Got signal %s" % sig)
    g_running=False

def log(arg,flush=False):
    print("LOG: %s" % arg)
    if(flush): sys.stdout.flush()

def usage(exit_system=True,exit_code=1):
    # Show the usage and exit
    print("python3 main.py -c configfile [-h]")
    sys.stdout.flush()
    if(exit_system):
        sys.exit(exit_code)
    return
def error_exit(msg="Error, exiting",exitcode=1):
    print(msg)
    sys.exit(exitcode)
    
''' Main system '''
def main(argv):
    global g_running

    config_file = "sample.conf"
    
    ### Process command line arguments
    try:
        opts, args = getopt.getopt(argv,"hc:",["conf="])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        #print("Found arg: %s -> %s" % (opt,arg))
        if opt == '-h':
            usage()
        elif opt in ("-c", "--conf"):
            config_file = str(arg)
    
    log("** Running")
    
    ### Load config
    conf = config.Config()    
    if(not config_file):
        print("Must have config file")
        usage()
    try:
        print("config: %s" % config_file)
        if(conf.load(config_file)==False):
            usage();
    except Exception as e:
        print("Error loading config: %s" % str(e))
        usage()
        
    # Parse the config file
    sec = "IoTConnect"
    cpid = conf.get_str(sec,"cpid");
    if(conf.strempty(cpid)): error_exit("Error, CPID is empty")
    env = conf.get_str(sec,"env");
    if(conf.strempty(env)): error_exit("Error, env is empty")

    sec = "Device"
    uniqueid = conf.get_str(sec,"uniqueid");
    if(conf.strempty(uniqueid)): error_exit("Error, UniqueID is empty")
    cert = conf.get_str(sec,"certificate");
    if(conf.strempty(cert)): error_exit("Error, certificate name is empty")
    key = conf.get_str(sec,"certificate_key");
    if(conf.strempty(key)): error_exit("Error, certificate key name is empty")
    
    # Show the settings
    print("\nSettings:\n--------------------")
    print("CPID: "+cpid)
    print("ENV: "+env)
    print("uniqueid: "+uniqueid)
    print("certificate: "+cert)
    print("certificate_key: "+key)
    print("")
    
    
    # Create the certificate structure the SDK expects
    SdkOptions={
    "certificate" : { 
        "SSLKeyPath" : key,  
        "SSLCertPath" : cert,
        "SSLCaPath" : cert
    }
    }

    #### System running
    try:
        
        # Create the SDK instance
        sdk = IoTConnectSDK(cpid, uniqueid, None, None,SdkOptions,env)
        
        # Loop while the program is running
        while(g_running):
            try:
                # Load data for all the attributes of this template
                data = {
                "Random_Integer": random.randint(1,100),
                } 
                
                # Load the attribute data in the expected format for IoTconnect
                dObj = [{
                    "uniqueId": uniqueid,
                    "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                    "data": data
                }]
                
                # If the SDK has connected to the server, send the data. Else
                # sleep for 5 seconds and try again
                if(sdk._is_process_started):
                    sdk.SendData(dObj)
                    print("Data sent, sleeping 60 seconds")
                    # Currently demo accounts of IoTConnect limit data transmit
                    # to once per 60 seconds. Contat IoTConnect administration
                    sleep_time=60;
                else:
                    print("Not connected, trying again in 5 seconds")
                    sleep_time=5;    
                
                # Sleep before looping again
                while(g_running and sleep_time>0):
                    time.sleep(1)
                    sleep_time-=1
                
            except Exception as e:
                print("Error with SDK: "+str(e))
        
        
    except Exception as e:
        print("Error with mainloop %s" % str(e))
        print("System shutting down")
    g_running = False
    
    log("** Normal exit")
    
    return


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main(sys.argv[1:])
