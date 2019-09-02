from machine import Pin
from machine import PWM
from time import sleep

class Speaker:
    def __init__(self, pin):
        self.speaker = PWM(Pin(pin))
        self.volume = 1

    def play_tone(self, frequency, duration=1):
        self.speaker.init(frequency, self.volume)
        sleep(duration)
        self.speaker.deinit()


s = Speaker(25)

s.play_tone(500, 0.5)
sleep(0.1)
s.play_tone(800, 0.5)
s.play_tone(500, 0.5)