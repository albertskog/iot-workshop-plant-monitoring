from machine import Pin
from machine import ADC
from machine import I2C
from dht import DHT11
from time import sleep
import network

from allthingstalk import AllThingsTalkDevice
from ssd1306 import SSD1306_I2C
from speaker import Speaker
from config import config

moisture = ADC(Pin(32))
moisture.atten(ADC.ATTN_11DB)
moisture_alarm_level = 10

temperature_humidity = DHT11(Pin(22))

light_sensor_power = Pin(32, Pin.OUT)
light_sensor_power.on()

light_sensor = ADC(Pin(35))
light_sensor.atten(ADC.ATTN_11DB)

i2c = I2C(scl = Pin(22), sda = Pin(21))
display = SSD1306_I2C(128, 64, i2c)
black = 0
white = 1

speaker = Speaker(Pin(26))

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

def read_sensors():
    sensor_data = {}

    # Read the moisture sensor and convert into percent
    sensor_data["moisture"] = int(100-(moisture.read()/40.96))

    # Read the DHT sensor
    temperature_humidity.measure()
    sensor_data["temperature"] = temperature_humidity.temperature()
    sensor_data["humidity"] = temperature_humidity.humidity()

    # Read light sensor
    sensor_data["light"] = int(light_sensor.read()/40.96)

    return sensor_data

while True:
    if wifi.isconnected():
        sensor_data = read_sensors()
        cloud.set_multiple(sensor_data)

        display.fill(black)

        message = "Moisture: {}%".format(sensor_data["moisture"])
        print(message)
        display.text(message, 10, 5)
        
        message = "Temp: {}C".format(sensor_data["temperature"])
        print(message)
        display.text(message, 10, 20)

        message = "Humidity: {}%".format(sensor_data["humidity"])
        print(message)
        display.text(message, 10, 35)

        message = "Light: {}%".format(sensor_data["light"])
        print(message)
        display.text(message, 10, 50)

        display.show()

        if sensor_data["moisture"] < moisture_alarm_level:
            speaker.play_tone(500)

        sleep(5)
    else:
        connect_wifi()
