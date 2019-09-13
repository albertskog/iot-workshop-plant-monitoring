from machine import Pin
from machine import ADC
from dht import DHT11
from time import sleep
import network

# These two imports are local files from this folder
from allthingstalk import AllThingsTalkDevice
from config import config

moisture = ADC(Pin(32))
moisture.atten(ADC.ATTN_11DB)

temperature_humidity = DHT11(Pin(22))

# Create an object for the connection to AllThingsTalk
cloud = AllThingsTalkDevice(config["device_id"], config["device_token"])

# Create an object for the wifi connection
wifi = network.WLAN(network.STA_IF)

# This is a function, it is called from the while-loop further down
def connect_wifi():
    wifi.active(True)
    if not wifi.isconnected():
        print('connecting to network...')
        wifi.connect(config["wifi_ssid"], config["wifi_password"])
        while not wifi.isconnected():
            pass
    print('network config:', wifi.ifconfig())

while True:
    if wifi.isconnected():
        # Read the moisture sensor and convert into percent
        moisture_percent = int(100-(moisture.read()/40.96))
        cloud.set_asset_state("moisture", moisture_percent)
        print("Moisture: {}%".format(moisture_percent))

        # Read the DHT sensor
        temperature_humidity.measure()

        temperature = temperature_humidity.temperature()
        cloud.set_asset_state("temperature", temperature)
        print("Temperature: {}".format(temperature))

        humidity = temperature_humidity.humidity()
        cloud.set_asset_state("humidity", humidity)
        print("Humidity: {}".format(humidity))

        sleep(5)
    else:
        connect_wifi()
