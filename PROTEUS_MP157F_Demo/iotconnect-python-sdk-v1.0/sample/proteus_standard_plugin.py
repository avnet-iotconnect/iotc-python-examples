import asyncio
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
import time
import sys

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
    "rms_speed_status_x": "Not_Available",
    "rms_speed_status_y": "Not_Available",
    "rms_speed_status_z": "Not_Available",
    "rms_speed_x_mmps": 0,
    "rms_speed_y_mmps": 0,
    "rms_speed_z_mmps": 0,
    "freq_status_x": "Not_Available",
    "freq_status_y": "Not_Available",
    "freq_status_z": "Not_Available",
    "freq_x_hz": 0,
    "freq_y_hz": 0,
    "freq_z_hz": 0,
    "freq_max_amp_x_ms2": 0,
    "freq_max_amp_y_ms2": 0,
    "freq_max_amp_z_ms2": 0,
    "accel_peak_status_x": "Not_Available",
    "accel_peak_status_y": "Not_Available",
    "accel_peak_status_z": "Not_Available",
    "accel_peak_x_ms2": 0,
    "accel_peak_y_ms2": 0,
    "accel_peak_z_ms2": 0
}

#These are the UUIDs of the BLE characteristics we use for the PROTEUS in this demo
temperature_characteristic = "00040000-0001-11e1-ac36-0002a5d5c51b"
accel_and_gyro_characteristic =  "00c00000-0001-11e1-ac36-0002a5d5c51b"
battery_characteristic = "00020000-0001-11e1-ac36-0002a5d5c51b"
rms_speed_characteristic = "00000007-0002-11e1-ac36-0002a5d5c51b"
peak_acceleration_characteristic = "00000008-0002-11e1-ac36-0002a5d5c51b"
freq_domain_characteristic = "00000009-0002-11e1-ac36-0002a5d5c51b"

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


#This function is called whenever a BLE packet from the temperature characteristic UUID is received
def temperature_data_handler(characteristic: BleakGATTCharacteristic, data:bytearray):
    global telemetry
    #Decode the temperature data and update the appropriate value in the telemetry dictionary
    telemetry["temperature_deg_C"] = int.from_bytes(data[2:4], "little")/10.0


#This function is called whenever a BLE packet from the battery characteristic UUID is received
def battery_data_handler(characteristic: BleakGATTCharacteristic, data:bytearray):
    global telemetry
    #Decode the battery data and update the appropriate values in the telemetry dictionary
    telemetry["battery_percentage"] = int.from_bytes(data[2:4], "little")/10.0
    telemetry["battery_voltage"] = int.from_bytes(data[4:6], "little")/1000.0
    telemetry["battery_current"] = int.from_bytes(data[6:8], "little")
    status_options = ["Low Battery", "Discharging", "Plugged not Charging", "Charging", "Unknown"]
    telemetry["battery_status"] = status_options[data[8]]

#This function is called whenever a BLE packet from the frequency domain characteristic UUID is received
def freq_domain_data_handler(characteristic: BleakGATTCharacteristic, data:bytearray):
    global telemetry
    status_options = ["Good", "Warning", "Alert"]
    #For the status values, we use a binary representation of the data
    data_binary_str = format(int.from_bytes((data)),'#0122b')[2:]
    #Decode the frequency domain data and update the appropriate values in the telemetry dictionary
    telemetry["freq_status_x"] = status_options[int(data_binary_str[18:20], 2)]
    telemetry["freq_status_y"] = status_options[int(data_binary_str[20:22], 2)]
    telemetry["freq_status_z"] = status_options[int(data_binary_str[22:24], 2)]
    telemetry["freq_x_hz"] = (struct.unpack('<H', data[3:5])[0])/10.0
    telemetry["freq_max_amp_x_ms2"] = (struct.unpack('<H', data[5:7])[0])/100.0
    telemetry["freq_y_hz"] = (struct.unpack('<H', data[7:9])[0])/10.0
    telemetry["freq_max_amp_y_ms2"] = (struct.unpack('<H', data[9:11])[0])/100.0
    telemetry["freq_z_hz"] = (struct.unpack('<H', data[11:13])[0])/10.0
    telemetry["freq_max_amp_z_ms2"] = (struct.unpack('<H', data[13:15])[0])/100.0


#This function is called whenever a BLE packet from the accelerometer/gyroscope characteristic UUID is received
def accel_gyro_data_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    global telemetry
    #Decode the accelerometer/gyroscope domain data and update the appropriate values in the telemetry dictionary
    telemetry["accel_x_mGs"] = int.from_bytes(data[2:4], byteorder='little', signed=True)/1000.0
    telemetry["accel_y_mGs"] = int.from_bytes(data[4:6], byteorder='little', signed=True)/1000.0
    telemetry["accel_z_mGs"] = int.from_bytes(data[6:8], byteorder='little', signed=True)/1000.0
    telemetry["gyro_x_dps"] = int.from_bytes(data[8:10], byteorder='little', signed=True)/10.0
    telemetry["gyro_y_dps"] = int.from_bytes(data[10:12], byteorder='little', signed=True)/10.0
    telemetry["gyro_z_dps"] = int.from_bytes(data[12:14], byteorder='little', signed=True)/10.0


#This function is called whenever a BLE packet from the peak acceleration characteristic UUID is received
def peak_accel_data_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    global telemetry
    status_options = ["Good", "Warning", "Alert"]
    #For the status values, we use a binary representation of the data
    data_binary_str = format(int.from_bytes((data)),'#0122b')[2:]
    #Decode the acceleration peak data and update the appropriate values in the telemetry dictionary
    telemetry["accel_peak_status_x"] = status_options[int(data_binary_str[18:20], 2)]
    telemetry["accel_peak_status_y"] = status_options[int(data_binary_str[20:22], 2)]
    telemetry["accel_peak_status_z"] = status_options[int(data_binary_str[22:24], 2)]
    telemetry["accel_peak_x_ms2"] = struct.unpack('<f', data[3:7])[0]
    telemetry["accel_peak_y_ms2"] = struct.unpack('<f', data[7:11])[0]
    telemetry["accel_peak_z_ms2"] = struct.unpack('<f', data[11:15])[0]
 

#This function is called whenever a BLE packet from the RMS speed characteristic UUID is received
def rms_speed_data_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    global telemetry
    status_options = ["Good", "Warning", "Alert"]
    #For the status values, we use a binary representation of the data
    data_binary_str = format(int.from_bytes((data)),'#0122b')[2:]
    #Decode the RMS speed data and update the appropriate values in the telemetry dictionary
    telemetry["rms_speed_status_x"] = status_options[int(data_binary_str[18:20], 2)]
    telemetry["rms_speed_status_y"] = status_options[int(data_binary_str[20:22], 2)]
    telemetry["rms_speed_status_z"] = status_options[int(data_binary_str[22:24], 2)]
    telemetry["rms_speed_x_mmps"] = struct.unpack('<f', data[3:7])[0]
    telemetry["rms_speed_y_mmps"] = struct.unpack('<f', data[7:11])[0]
    telemetry["rms_speed_z_mmps"] = struct.unpack('<f', data[11:15])[0]


#This asynchronous function connects the gateway to the PROTEUS via BLE 
#and turns on the notifications for the desired characteristics
async def proteus_functionality():
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
        await client.start_notify(accel_and_gyro_characteristic, accel_gyro_data_handler)
        await client.start_notify(rms_speed_characteristic, rms_speed_data_handler)
        await client.start_notify(peak_acceleration_characteristic, peak_accel_data_handler)
        await client.start_notify(freq_domain_characteristic, freq_domain_data_handler)
        await client.start_notify(temperature_characteristic, temperature_data_handler)
        await client.start_notify(battery_characteristic, battery_data_handler)
	# Start an infinite loop so that notifications are received forever (until the program is shut down)
        while True:
            await asyncio.sleep(1)

#This loop is what the dedicated proteus thread will run when started in the main loop
def proteus_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    #Runs the func
    loop.run_until_complete(proteus_functionality())
    loop.close()
