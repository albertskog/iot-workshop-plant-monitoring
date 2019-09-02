from machine import Pin, Signal
from time import sleep

led = Signal(16, Pin.OUT, invert=True)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)