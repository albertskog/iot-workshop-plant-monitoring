from machine import Pin
from dht import DHT11
from time import sleep

sensor = DHT11(Pin(22))

while True:
    sensor.measure()
    print("Temperature: {}  Humidity: {}".format(sensor.temperature(), sensor.humidity()))
    sleep(1)