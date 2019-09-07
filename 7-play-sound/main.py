from machine import Pin
from time import sleep
from speaker import Speaker

speaker = Speaker(Pin(26))

speaker.play_tone(500)

sleep(0.5)

for i in range(10):
    frequency = 500 + 100 * i
    speaker.play_tone(frequency, duration = 0.1)

sleep(0.5)

for i in range(10):
    frequency = 1500 - 100 * i
    speaker.play_tone(frequency, duration = 0.1)