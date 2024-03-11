import asyncio
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
import time
import sys
import pexpect
import traceback

def debug_print_to_file(target_string):
    timestamp = str(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + " ///// " )
    with open('debug_print_output.txt', 'a') as debug_file:
        debug_file.write(timestamp + target_string + '\n')

#This dictionary is what the main loop of the main 
#program will periodcially send as telemetry to IoTConnect
telemetry = {
    "temperature_deg_C":0,
    "battery_percentage":0,
    "battery_voltage":0,
    "battery_current":0,
    "battery_status": "Not_Available",
    "accel_x_mGs":0,
    "accel_y_mGs":0,
    "accel_z_mGs":0,
    "gyro_x_dps":0,
    "gyro_y_dps":0,
    "gyro_z_dps":0,
    "magnet_x_mGa":0,
    "magnet_y_mGa":0,
    "magnet_z_mGa":0,
    "pressure_mBar":0
}

#These are the UUIDs of the BLE characteristics we use for the MKBOXPRO in this demo
temperature_pressure_characteristic = "00140000-0001-11e1-ac36-0002a5d5c51b"
accel_gyro_magnet_characteristic =  "00e00000-0001-11e1-ac36-0002a5d5c51b"
battery_characteristic = "00020000-0001-11e1-ac36-0002a5d5c51b"

#This function resets the bluetooth system to make 
#sure that no devices are connected at the start of the program
def setup_bluetooth():
    try:
        setup_process = pexpect.spawn('bluetoothctl', encoding='utf-8')
        setup_process.expect('#')
        setup_process.sendline('power off')
        time.sleep(1)
        setup_process.sendline('power on')
        time.sleep(1)
        setup_process.close()
    except Exception as ex:
        debug_print_to_file("setup_bluetooth exception: " + str(ex))
        debug_print_to_file(str(traceback.format_exc()))


#This function is called whenever a BLE packet from the temperature/pressure characteristic UUID is received
def temperature_pressure_data_handler(characteristic: BleakGATTCharacteristic, data:bytearray):
    global telemetry
    try:
        #Decode the temperature data and update the appropriate value in the telemetry dictionary
        telemetry["pressure_mBar"] = int.from_bytes(data[2:6], "little")/100.0
        telemetry["temperature_deg_C"] = int.from_bytes(data[6:8], "little")/10.0
    except Exception as ex:
        debug_print_to_file("temperature_pressure_data_handler exception: " + str(ex))
        debug_print_to_file(str(traceback.format_exc()))


#This function is called whenever a BLE packet from the battery characteristic UUID is received
def battery_data_handler(characteristic: BleakGATTCharacteristic, data:bytearray):
    global telemetry
    try:
        #Decode the battery data and update the appropriate values in the telemetry dictionary
        telemetry["battery_percentage"] = int.from_bytes(data[2:4], "little")/10.0
        telemetry["battery_voltage"] = int.from_bytes(data[4:6], "little")/1000.0
        telemetry["battery_current"] = int.from_bytes(data[6:8], "little")
        status_options = ["Low Battery", "Discharging", "Plugged not Charging", "Charging", "Unknown"]
        telemetry["battery_status"] = status_options[data[8]]
    except Exception as ex:
        debug_print_to_file("battery_data_handler exception: " + str(ex))
        debug_print_to_file(str(traceback.format_exc()))	


#This function is called whenever a BLE packet from the accelerometer/gyroscope/magnetometer characteristic UUID is received
def accel_gyro_magnet_data_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    global telemetry
    try:
        #Decode the accelerometer/gyroscope domain data and update the appropriate values in the telemetry dictionary
        telemetry["accel_x_mGs"] = int.from_bytes(data[2:4], byteorder='little', signed=True)
        telemetry["accel_y_mGs"] = int.from_bytes(data[4:6], byteorder='little', signed=True)
        telemetry["accel_z_mGs"] = int.from_bytes(data[6:8], byteorder='little', signed=True)
        telemetry["gyro_x_dps"] = int.from_bytes(data[8:10], byteorder='little', signed=True)
        telemetry["gyro_y_dps"] = int.from_bytes(data[10:12], byteorder='little', signed=True)
        telemetry["gyro_z_dps"] = int.from_bytes(data[12:14], byteorder='little', signed=True)
        telemetry["magnet_x_mGa"] = int.from_bytes(data[14:16], byteorder='little', signed=True)
        telemetry["magnet_y_mGa"] = int.from_bytes(data[16:18], byteorder='little', signed=True)
        telemetry["magnet_z_mGa"] = int.from_bytes(data[18:20], byteorder='little', signed=True)
    except Exception as ex:
        debug_print_to_file("accel_gyro_magnet_data_handler exception: " + str(ex))
        debug_print_to_file(str(traceback.format_exc()))


#This asynchronous function connects the gateway to the MKBOXPRO via BLE 
#and turns on the notifications for the desired characteristics
async def main_functionality():
    try:
        #Reset the bluetooth system
        setup_bluetooth()
        print("starting scan...")
        #Scan for the PMKBOXPRO BLE device by name
        device = await BleakScanner.find_device_by_name("BLEPnP")
        if device is None:
            print("ERROR: could not find device with name '%s'", args.name)
            return
        print("connecting to device...")
        #With the MKBOXPRO device connected
        async with BleakClient(device) as client:
            print("Connected")
	    #Turn on notifications for the desire characteristics
            await client.start_notify(accel_gyro_magnet_characteristic, accel_gyro_magnet_data_handler)
            await client.start_notify(temperature_pressure_characteristic, temperature_pressure_data_handler)
            await client.start_notify(battery_characteristic, battery_data_handler)
	    # Start an infinite loop so that notifications are received forever (until the program is shut down)
            while True:
                await asyncio.sleep(1)
    except Exception as ex:
        debug_print_to_file("mkboxpro_functionality exception: " + str(ex))
        debug_print_to_file(str(traceback.format_exc()))

#This loop is what the dedicated proteus thread will run when started in the main loop
def main_loop():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        #Runs the func
        loop.run_until_complete(main_functionality())
        loop.close()
    except Exception as ex:
        debug_print_to_file("mkboxpro_loop exception: " + str(ex))
        debug_print_to_file(str(traceback.format_exc()))   
