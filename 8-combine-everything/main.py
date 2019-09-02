from machine import Pin
from machine import ADC
from time import sleep
from allthingstalk import AllThingsTalkDevice
import network

wlan = network.WLAN(network.STA_IF)
device_id = ""
device_token = "maker:"

cloud = AllThingsTalkDevice(device_id, device_token)

moisture = ADC(Pin(32))
moisture.atten(ADC.ATTN_11DB)

def do_connect():
    
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('ssid', 'password')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

while True:
    if wlan.isconnected():
        cloud.set_asset_state("Moisture", int(100-(moisture.read()/40.96)))
        print(".")
        sleep(5)
    else:
        do_connect()
