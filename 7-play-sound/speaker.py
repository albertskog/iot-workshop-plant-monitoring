from machine import Pin
from machine import PWM
from time import sleep

class Speaker:
    def __init__(self, pin):
        self.speaker = PWM(pin)
        self.volume = 1

    def play_tone(self, frequency, duration=1):
        self.speaker.init(frequency, self.volume)
        sleep(duration)
        self.speaker.deinit()
