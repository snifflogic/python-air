# ble communciation
import asyncio
from bleak import BleakScanner, BleakGATTCharacteristic
# printing time
import time
#pretty printing
from rich import print
# model
from air import Air
from datapoint import DataPoint

## variables
# input from user
command = 0
# address of air
address = ""
# time we started acquiring data
startTime = 0



def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    """notification handler that prints the time and the parsed data received
    The arguments are passed automatically by bleak

    Args:
        characteristic (BleakGATTCharacteristic): The characteristic being read
        data (bytearray): data recieved: 8 bytes of data
    """
    global startTime
    # parse data
    point = DataPoint(data);
    # calculate time from start in seconds  
    data_time = (time.time_ns()-startTime)/1000000000 
    # print
    print(f"\[time(s): {data_time:.4f}, {point}]")

async def main():
    """main script:
     - scan for devices
     - user chooses the Air from a list
     - connect to the Air
     - read battery level
     - read and write sampling rate
     - acquire 5 seconds of live data
     - change the Air name
     - disconnect
    """
    global address
    global command
    global startTime
    # scan for devices
    while (command == 0 ):
        i = 1 # list index
        print("Scanning for devices...")
        devices = await BleakScanner.discover()
        print("Device list: ")
        for device in devices:
            print(f" {i} {device}")
            i = i+1
        print("Enter number to connect to device, 0 to retry, 99 to quit")
        input_str = input()
        try:
            command = int(input_str)
        except:
            print("Did not understand, retrying")
        if (command == 99):
            exit()
        if (command != 0):
            address = devices[command-1]
    print(f"Connecting to: {address}...")
    # connect to chosen device
    air = Air(address)
    try:
        # connect
        await air.connect() 
        # print all the services and characteristics     
        air.print_all_characteristics()
        # get battery level
        batterylevel = await air.get_battery()
        print(f"battery level: {batterylevel}%")
        # get current sampling rate (default is 6)
        freq = await air.get_frequency()
        print(f"frequency: {freq}Hz")
        # change sampling rate
        await air.set_frequency(15)
        # confirm rate changed
        freq = await air.get_frequency()
        print(f"New frequency: {freq}Hz")
        # get data at new rate for 5 seconds
        startTime = time.time_ns()
        await air.subscribe(notification_handler)
        await asyncio.sleep(5.0)
        await air.unsubscribe()
        # change name of air - will be seen only after disconnect and reconnect
        await air.change_name("AirNew")

    except Exception as e:
        print(e)
    finally:
        await air.disconnect()

# run main asynchrounously
asyncio.run(main())