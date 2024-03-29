import asyncio
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
import time
import sys
import pexpect

# Anomaly Detection mode can either be "Learning" or "Detection"
AD_Mode = "Learning"
# Anomaly Detection can be either be "On" or "Off"
AD_OnOff = "Off"
# Knowledge Reset button is either "Normal" or "Pressed"
Knowledge_Reset_Button = "Normal"

#This dictionary is what the main loop of the main 
#program will periodcially send as telemetry to IoTConnect
telemetry = {
    "battery_percentage":0,
    "battery_voltage":0,
    "battery_current":0,
    "battery_status":"Not_Available",
    "NEAI_phase":"Not yet specified",
    "NEAI_state":"Not yet specified",
    "NEAI_progress_percentage":0,
    "NEAI_status":"Not yet specified",
    "NEAI_similarity_percentage":0
}


#These are the UUIDs of the BLE characteristics we use for the PROTEUS in this demo
battery_characteristic = "00020000-0001-11e1-ac36-0002a5d5c51b"
anomaly_detection_characteristic = "00000019-0002-11e1-ac36-0002a5d5c51b"


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


#This function is called whenever a BLE packet from the battery characteristic UUID is received
def battery_data_handler(characteristic: BleakGATTCharacteristic, data:bytearray):
    global telemetry
    #Decode the battery data and update the appropriate values in the telemetry dictionary
    telemetry["battery_percentage"] = int.from_bytes(data[2:4], "little")/10.0
    telemetry["battery_voltage"] = int.from_bytes(data[4:6], "little")/1000.0
    telemetry["battery_current"] = int.from_bytes(data[6:8], "little")
    status_options = ["Low Battery", "Discharging", "Plugged not Charging", "Charging", "Unknown"]
    telemetry["battery_status"] = status_options[data[8]]

#This function is called whenever a BLE packet from the anomaly detection characteristic UUID is received
def anomaly_detection_data_handler(characteristic: BleakGATTCharacteristic, data:bytearray):
    global telemetry
    #Decode the anomaly detection data and update the appropriate values in the telemetry dictionary
    NEAI_phase_options = ["Idle", "Learning", "Detecting"]
    if data[4] != 0xFF:
        telemetry["NEAI_phase"] = NEAI_phase_options[data[4]]
    else:
        telemetry["NEAI_phase"] = "Not currently available"
    NEAI_state_options = ["NEAI_OK"]
    if data[5] != 0xFF:
        telemetry["NEAI_state"] = NEAI_state_options[data[5]]
    else:
        telemetry["NEAI_state"] = "Not currently available"
    telemetry["NEAI_progress_percentage"] = int.from_bytes(data[6], "little")
    NEAI__status_options = ["Normal", "Anomaly"]
    if data[7] != 0xFF:
        telemetry["NEAI_status"] = NEAI_status_options[data[7]]
    else:
        telemetry["NEAI_status"] = "Not currently available"
    telemetry["NEAI_similarity_percentage"] = int.from_bytes(data[8], "little")

#This asynchronous function connects the gateway to the PROTEUS via BLE 
#and turns on the notifications for the desired characteristics
async def main_functionality():
    #Reset the bluetooth system
    setup_bluetooth()
    print("starting scan...")
    #Scan for the PROTEUS BLE device by name
    device = await BleakScanner.find_device_by_name("PROTEUS")
    if device is None:
        print("ERROR: could not find device with name '%s'", args.name)
        return
    print("connecting to device...")
    #With the PROTEUS device connected
    async with BleakClient(device) as client:
        print("Connected")
	#Turn on notifications for the desire characteristics
        await client.start_notify(battery_characteristic, battery_data_handler)
        await client.start_notify(anomaly_detection_characteristic, anomaly_detection_data_handler)
	# Start an infinite loop so that notifications are received forever (until the program is shut down)
        while True:
            await asyncio.sleep(1)


#This loop is what the dedicated proteus thread will run when started in the main loop
def main_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    #Runs the func
    loop.run_until_complete(main_functionality())
    loop.close()
