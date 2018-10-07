from RPi import GPIO
from threading import Timer

class Led:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
    
    def on(self, duration = 0):
        GPIO.output(self.pin, GPIO.HIGH)
        if duration > 0:
            t = Timer(duration, self.off)
            t.start()
    
    def off(self):
        GPIO.output(self.pin, GPIO.LOW)


"""
from time import sleep
GPIO.setmode(GPIO.BCM)
red = Led(19)
green = Led(17)
blue = Led(27)
yellow = Led(22)

red.on(0.25)
sleep(1)
green.on(0.25)
sleep(1)
blue.on(0.25)
sleep(1)

yellow.on()
sleep(2)
yellow.off()

GPIO.cleanup()
"""