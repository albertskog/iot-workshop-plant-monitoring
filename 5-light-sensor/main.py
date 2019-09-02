from machine import Pin
from machine import ADC
from time import sleep

light_sensor_power = Pin(32, Pin.OUT)
light_sensor_power.on()

light_sensor = ADC(Pin(35))
light_sensor.atten(ADC.ATTN_11DB)

while True:
    print(light_sensor.read())
    sleep(1)