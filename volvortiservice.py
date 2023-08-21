"""Maury Knudsen
March 2022
2004 Volvo V70 RTI retrofit with RP open auto pro/raspbian build
"""


import serial
import pyudev
import time

#open uart serial, rti baudrate=2400
ser = serial.Serial('/dev/ttyAMA0', 2400)

#set up usb monitoring from pyudev
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')
monitor.start()

#array to store usb model ids
model_ids = []
trigger = 0

while True:
    #check for device added to usb
    for device in iter(monitor.poll, None):
        if device.action == "add":
            trigger = 1
            break
    while trigger == 1:
        #reset array to check devices
        model_ids.clear()
        #send bytes to rti to raise screen, need 100ms delay
        ser.write(bytearray([0x45]))
        time.sleep(0.1)
        ser.write(bytearray([0x2F]))
        time.sleep(0.1)
        ser.write(bytearray([0x83]))
        time.sleep(0.1)
        #check for phone unplug to end loop/lower screen
        for device in context.list_devices(subsystem='usb'):
            model_ids.append(device.get('ID_MODEL'))
        if "motorola_one_5G" not in model_ids:
            trigger = 0
        