from machine import Pin
from machine import ADC
from time import sleep

moisture = ADC(Pin(32))
moisture.atten(ADC.ATTN_11DB)

while True:
    print(moisture.read())
    sleep(1)