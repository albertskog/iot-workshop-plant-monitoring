from machine import Pin
from machine import ADC
from machine import I2C
from dht import DHT11
from time import sleep
import network

from allthingstalk import AllThingsTalkDevice
from ssd1306 import SSD1306_I2C
from config import config

moisture = ADC(Pin(32))
moisture.atten(ADC.ATTN_11DB)

temperature_humidity = DHT11(Pin(22))

light_sensor_power = Pin(32, Pin.OUT)
light_sensor_power.on()

light_sensor = ADC(Pin(35))
light_sensor.atten(ADC.ATTN_11DB)

i2c = I2C(scl = Pin(22), sda = Pin(21))
display = SSD1306_I2C(128, 64, i2c)
black = 0
white = 1

cloud = AllThingsTalkDevice(config["device_id"], config["device_token"])

wifi = network.WLAN(network.STA_IF)

def connect_wifi():
    wifi.active(True)
    if not wifi.isconnected():
        print("Connecting to wifi...")
        display.fill(black)
        display.text("Connecting", 10, 20)
        display.text("to wifi...", 10, 35)
        display.show()
        wifi.connect(config["wifi_ssid"], config["wifi_password"])
        while not wifi.isconnected():
            pass
    print("Network config:", wifi.ifconfig())

while True:
    if wifi.isconnected():
        display.fill(black)

        # Read the moisture sensor and convert into percent
        moisture_percent = int(100-(moisture.read()/40.96))
        cloud.set_asset_state("moisture", moisture_percent)
        message = "Moisture: {}%".format(moisture_percent)
        print(message)
        display.text(message, 10, 5)

        # Read the DHT sensor
        temperature_humidity.measure()

        temperature = temperature_humidity.temperature()
        cloud.set_asset_state("temperature", temperature)
        message = "Temp: {}C".format(temperature)
        print(message)
        display.text(message, 10, 20)

        humidity = temperature_humidity.humidity()
        cloud.set_asset_state("humidity", humidity)
        message = "Humidity: {}%".format(humidity)
        print(message)
        display.text(message, 10, 35)

        # Read light sensor
        light_percent = int(light_sensor.read()/40.96)
        cloud.set_asset_state("light", light_percent)
        message = "Light: {}".format(light_percent)
        print(message)
        display.text(message, 10, 50)

        display.show()

        sleep(5)
    else:
        connect_wifi()
