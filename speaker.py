from RPi import GPIO
from threading import Timer

class Speaker:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.frequency = 0
    
    def play(self, frequency, duration = 0):
        if self.frequency == 0:
            self.frequency = frequency
            self.pwm = GPIO.PWM(self.pin, self.frequency)
        else:
            self.frequency = frequency
            self.pwm.stop()
            self.pwm.ChangeFrequency(self.frequency)
        self.pwm.start(50.0)
        if duration > 0:
            t = Timer(duration, self.stop)
            t.start()
    def stop(self):
        self.pwm.stop()

"""
from time import sleep
GPIO.setmode(GPIO.BCM)
mySpeaker = Speaker(13)

mySpeaker.play(250, 0.25)
sleep(1)
mySpeaker.play(250, 0.25)
sleep(1)
mySpeaker.play(250, 0.25)
sleep(1)

mySpeaker.play(250)
sleep(2)
mySpeaker.stop()

GPIO.cleanup()
"""