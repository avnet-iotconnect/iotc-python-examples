import argparse
import asyncio
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
import struct
import pexpect
import time
import sys

telemetry = {
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

temperature_characteristic = "00040000-0001-11e1-ac36-0002a5d5c51b"
accel_and_gyro_characteristic =  "00c00000-0001-11e1-ac36-0002a5d5c51b"
battery_characteristic = "00020000-0001-11e1-ac36-0002a5d5c51b"
rms_speed_characteristic = "00000007-0002-11e1-ac36-0002a5d5c51b"
peak_acceleration_characteristic = "00000008-0002-11e1-ac36-0002a5d5c51b"
freq_domain_characteristic = "00000009-0002-11e1-ac36-0002a5d5c51b"

def setup_bluetooth():
    setup_process = pexpect.spawn('bluetoothctl', encoding='utf-8')
    setup_process.expect('#')
    setup_process.sendline('power off')
    time.sleep(1)
    setup_process.sendline('power on')
    time.sleep(1)
    setup_process.close()

def temperature_data_handler(characteristic: BleakGATTCharacteristic, data:bytearray):
    pass

def battery_data_handler(characteristic: BleakGATTCharacteristic, data:bytearray):
    pass

def freq_domain_data_handler(characteristic: BleakGATTCharacteristic, data:bytearray):
    global telemetry
    status_options = ["Good", "Warning", "Alert"]
    data_binary_str = format(int.from_bytes((data)),'#0122b')[2:]
    telemetry["freq_status_x"] = status_options[int(data_binary_str[18:20], 2)]
    telemetry["freq_status_y"] = status_options[int(data_binary_str[20:22], 2)]
    telemetry["freq_status_z"] = status_options[int(data_binary_str[22:24], 2)]
    telemetry["freq_x_hz"] = (struct.unpack('<H', data[3:5])[0])/10.0
    telemetry["freq_max_amp_x_ms2"] = (struct.unpack('<H', data[5:7])[0])/100.0
    telemetry["freq_y_hz"] = (struct.unpack('<H', data[7:9])[0])/10.0
    telemetry["freq_max_amp_y_ms2"] = (struct.unpack('<H', data[9:11])[0])/100.0
    telemetry["freq_z_hz"] = (struct.unpack('<H', data[11:13])[0])/10.0
    telemetry["freq_max_amp_z_ms2"] = (struct.unpack('<H', data[13:15])[0])/100.0

		
def accel_gyro_data_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    global telemetry
    telemetry["accel_x_mGs"] = int.from_bytes(data[2:4], byteorder='little', signed=True)/1000.0
    telemetry["accel_y_mGs"] = int.from_bytes(data[4:6], byteorder='little', signed=True)/1000.0
    telemetry["accel_z_mGs"] = int.from_bytes(data[6:8], byteorder='little', signed=True)/1000.0
    telemetry["gyro_x_dps"] = int.from_bytes(data[8:10], byteorder='little', signed=True)/10.0
    telemetry["gyro_y_dps"] = int.from_bytes(data[10:12], byteorder='little', signed=True)/10.0
    telemetry["gyro_z_dps"] = int.from_bytes(data[12:14], byteorder='little', signed=True)/10.0
    
    
def peak_accel_data_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    global telemetry
    status_options = ["Good", "Warning", "Alert"]
    data_binary_str = format(int.from_bytes((data)),'#0122b')[2:]
    telemetry["accel_peak_status_x"] = status_options[int(data_binary_str[18:20], 2)]
    telemetry["accel_peak_status_y"] = status_options[int(data_binary_str[20:22], 2)]
    telemetry["accel_peak_status_z"] = status_options[int(data_binary_str[22:24], 2)]
    telemetry["accel_peak_x_ms2"] = struct.unpack('<f', data[3:7])[0]
    telemetry["accel_peak_y_ms2"] = struct.unpack('<f', data[7:11])[0]
    telemetry["accel_peak_z_ms2"] = struct.unpack('<f', data[11:15])[0]
 
    
def rms_speed_data_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    global telemetry
    status_options = ["Good", "Warning", "Alert"]
    data_binary_str = format(int.from_bytes((data)),'#0122b')[2:]
    telemetry["rms_speed_status_x"] = status_options[int(data_binary_str[18:20], 2)]
    telemetry["rms_speed_status_y"] = status_options[int(data_binary_str[20:22], 2)]
    telemetry["rms_speed_status_z"] = status_options[int(data_binary_str[22:24], 2)]
    telemetry["rms_speed_x_mmps"] = struct.unpack('<f', data[3:7])[0]
    telemetry["rms_speed_y_mmps"] = struct.unpack('<f', data[7:11])[0]
    telemetry["rms_speed_z_mmps"] = struct.unpack('<f', data[11:15])[0]


async def proteus_reporting_loop():
    setup_bluetooth()
    print("starting scan...")
    device = await BleakScanner.find_device_by_name("PROTEUS")
    if device is None:
        print("ERROR: could not find device with name '%s'", args.name)
        return
    print("connecting to device...")
    async with BleakClient(device) as client:
        print("Connected")
        await client.start_notify(accel_and_gyro_characteristic, accel_gyro_data_handler)
        await client.start_notify(rms_speed_characteristic, rms_speed_data_handler)
        await client.start_notify(peak_acceleration_characteristic, peak_accel_data_handler)
        await client.start_notify(freq_domain_characteristic, freq_domain_data_handler)
        while True:
            await asyncio.sleep(1)


def data_transfer():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(proteus_reporting_loop())
    loop.close()
