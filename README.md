# python-air
Python SDK for communicating with the Sniff Controller Air of Sniff Logic

# Usage
Clone this repository to your computer. To run this example, execute `example.py`. The script scans for ble devices and presents a list. 
Choose the device number you wish to connect to. The script will then retrieve the battery level and sample rate, modify the sample rate, acquire 5 seconds of data, and print it. It will also change the name (visible only after disconnecting and rescanning).  

![Alt text](image.png)

To use in your own project, copy `air.py` and `datapoint.py` into your project folder and import `Air` and DataPoint into your file.

- `air.py`  - represents the Air device. 
- `datapoint.py` - represents a single data point acquired by the Air, including both the breathing and accelerometer data.
- `example.py` - a script demonstrating how to use the Air and DataPoint classes

# Packages
[`bleak`](https://bleak.readthedocs.io/en/latest/) - for communicating with BLE device
[`rich`](https://rich.readthedocs.io/en/stable/introduction.html) -  for pretty printing. It can be omitted (simply remove the import statement if omitting).

# Bugs
If you've encountered a bug, please open an issue. Include details about your device, operating system, Python version, and Bluetooth version on your computer. Don't forget to attach your code.

# Contribute
Have you implemented something useful that could benefit others? Don't hesitate to submit a pull request.