import sys
import json
import time
import threading
import random
from datetime import datetime
import os
sys.path.append("/home/weston/STM32MP157F_Demo")
sys.path.append("/home/weston/STM32MP157F_Demo/plugins")
import proteus_AI_plugin

def main():
    try:
        sensor_thread = threading.Thread(target=proteus_AI_plugin.main_loop)
        sensor_thread.start()
        while True:
            dObj = [{
                "data": proteus_AI_plugin.telemetry
            }]
            print(dObj)
                    
    except KeyboardInterrupt:
        print ("Keyboard Interrupt Exception")
        sys.exit(0)
                 
    except Exception as ex:
        print(ex)
        sys.exit(0)

if __name__ == "__main__":
    main()
