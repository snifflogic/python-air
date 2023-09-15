from typing import Awaitable, Callable
from bleak import BleakClient, BleakGATTCharacteristic

## UUIDs of characterstics of the Air
DATA_UUID = "00000001-c221-03d1-2336-9112fd7a556b"
FREQUENCY_UUID = "00000010-C221-03D1-2336-9112FD7A556B"
BATTERY_UUID = "00002a19-0000-1000-8000-00805f9b34fb"
NAME_UUID = "00000001-C221-03D1-2336-9112FD7A556C"

class Air:
     """Class for communicating with the Sniff Controller Air
     """
     def __init__(self, address: str) -> None:
          """Create a new Air with the given address

          Args:
             address (str): the Bluetooth address of the air, 
             as a hex string separated by colons, e.g. `72:29:35:7E:8E:70:`
          """
          self.client = BleakClient(address)
          self.connected = False
        
     async def connect(self):
          """attempt to connect to the air. may raise an exception of cannot connect.
          """
          await self.client.connect()
          self.connected = True

     def print_all_characteristics(self):
          """Prints out all the services and characteristics of the Air
          """
          if (self.connected):
            for service in self.client.services:
                print(f"[Service] {service}")
                for char in service.characteristics:
                    print(f"[char] {char.uuid}")
          else:
               print ("Not connected")
    
     async def get_battery(self) -> int:
          """Reads the battery level of this Air in percent.

          Returns:
              int: battery level in percent.
          """
          data = await self.client.read_gatt_char(BATTERY_UUID)
          return data[0]
    
     async def get_frequency(self) -> int:
          """Reads the sampling rate (frequency) of this Air in Hz

          Returns:
              int: sampling rate in Hz
          """
          data = await self.client.read_gatt_char(FREQUENCY_UUID)
          return data[0]
    
     async def set_frequency(self, newFreq: int) -> None:
          """Sets the sampling rate of this Air.
          IMPORTANT! currently the Air supports 6 or 15 Hz only.

          Args:
              newFreq (int): new Fequency, must be 6 or 15

          Raises:
              Exception: if newInt is not 6 or 15
          """
          if newFreq != 6 and newFreq != 15:
              raise Exception ("The air currently supports 6Hz or 15Hz sampling rate only")
          await self.client.write_gatt_char(FREQUENCY_UUID,newFreq.to_bytes(1,byteorder='little',signed=False), response=True)
    
     async def change_name(self, newName: str):
          """Changes the name of the Air so that subsequent BLE scans will see it with a different human-readable name. 
          The address is not affected by this change. In order to see the changem it is necessary to disconnect and scan again.
          IMPORTANT! In order to preserve compatibility with our software, the name MUST start with 'Air'.
          Also, The total length of the name must be no more than 8 characters.

          Args:
              newName (str): New name of Air

          Raises:
              Exception: if name doesn't start with `Air` or is too long.
          """
          if not newName.startswith("Air"):
               raise Exception ("Name of Air device must start with 'Air' for compatibility reasons")
          if not len(newName) <= 8:
               raise Exception ("Length of new name must be less than or equal to 8")

          await self.client.write_gatt_char(NAME_UUID,newName.encode(), response=True)
         
    
     async def subscribe(self, notification_handler: Callable[[BleakGATTCharacteristic, bytearray], (Awaitable[None] | None)]):
          """Subscribes to data (breathing and accelerometer)

          Args:
              notification_handler ([BleakGATTCharacteristic, bytearray], (Awaitable[None] | None)]): Function that handles incoming data when it is received. 
              Use the DataPoint class to parse the incoming data.
          """
          await self.client.start_notify(DATA_UUID,notification_handler)

     async def unsubscribe(self):
          """unsubscribe to data
          """
          await self.client.stop_notify(DATA_UUID)
    
     async def disconnect(self):
          """Disconnects from the air
          """
          await self.client.disconnect()
          self.connected = False
