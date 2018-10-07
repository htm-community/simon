from RPi import GPIO

class Button:
    def __init__(self, index, pin, callback):
        self.index = index
        self.pin = pin
        self.callback = callback
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, self.internalcb)
        self.state = False
    
    def internalcb(self, channel):
        if GPIO.input(self.pin):
            if not self.state:
                self.state = True
                self.callback(self.index, self.state)
        else:
            if self.state:
                self.state = False
                self.callback(self.index, self.state)

"""
GPIO.setmode(GPIO.BCM)
def btncallback(index, state):
    if state:
        print "Button " + str(index) + " pressed"
    else:
        print "Button " + str(index) + " released"
        
resetButton = Button(0, 10, btncallback)
redButton = Button(1, 9, btncallback)
greenButton = Button(2, 11, btncallback)
blueButton = Button(3, 5, btncallback)
yellowButton = Button(4, 6, btncallback)

raw_input( "Press Enter to quit" )
GPIO.cleanup()
"""