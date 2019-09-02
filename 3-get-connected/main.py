from machine import Pin
from machine import ADC
from time import sleep
import network

# These two imports are local files from this folder
from allthingstalk import AllThingsTalkDevice
from config import config

# Create an object for the connection to AllThingsTalk
cloud = AllThingsTalkDevice(config["device_id"], config["device_token"])

# Create an object for the wifi connection
wifi = network.WLAN(network.STA_IF)

# This is a function, it is called from the while-loop further down
def connect_wifi():
    wifi.active(True)
    if not wifi.isconnected():
        print("Connecting to wifi...")
        wifi.connect(config["wifi_ssid"], config["wifi_password"])
        while not wifi.isconnected():
            pass
    print('Network config:', wifi.ifconfig())


# Here is the main loop that will run continously
counter = 0
while True:
    if wifi.isconnected():
        cloud.set_asset_state("counter", counter)
        print("Counter sent: {}".format(counter))
        counter += 1
        sleep(5)
    else:
        connect_wifi()
