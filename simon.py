import numpy
from nupic.algorithms.temporal_memory import TemporalMemory
from time import sleep
from led import Led
from button import Button
from speaker import Speaker
from RPi import GPIO

GPIO.setmode(GPIO.BCM)
mode = 0

tm = TemporalMemory(columnDimensions = (200,),
                    cellsPerColumn = 32,
                    initialPermanence = 0.5,
                    connectedPermanence = 0.5,
                    minThreshold = 10,
                    maxNewSynapseCount = 32,
                    permanenceIncrement = 0.1,
                    permanenceDecrement = 0.1,
                    activationThreshold = 13,
                    )

inputSDRs = numpy.zeros((5, tm.numberOfColumns()), dtype = "uint32")
for x in range(5):
    inputSDRs[x, (x*40):((x+1)*40)] = 1

inputColumns = []
for x in range(5):
    inputColumns.append(set([c for c, i in enumerate(inputSDRs[x]) if i == 1]))

ledPins = [26, 19, 17, 27, 22]
leds = []
for x in range(5):
    leds.append(Led(ledPins[x]))

tones = [0, 220, 262, 330, 440]
speaker = Speaker(13)

def unfold():
    global mode, tm, leds, speaker
    tm.reset()
    tm.compute(inputColumns[0], learn = False)
    predictiveColumns = [tm.columnForCell(i) for i in tm.getPredictiveCells()]
    while len(predictiveColumns) > 0:
        prediction = predictiveColumns[0] / 40
        leds[prediction].on(0.25)
        speaker.play(tones[prediction], 0.25)
        sleep(0.5)
        tm.compute(inputColumns[prediction], learn = False)
        predictiveColumns = [tm.columnForCell(i) for i in tm.getPredictiveCells()]
    tm.reset()
    tm.compute(inputColumns[0], learn = True)
    mode = 1

bursting = False
def buttoncb(index, state):
    global mode, tm, leds, speaker, bursting
    if index == 0:
        mode = 0
        tm = TemporalMemory(columnDimensions = (200,),
                            cellsPerColumn = 32,
                            initialPermanence = 0.5,
                            connectedPermanence = 0.5,
                            minThreshold = 10,
                            maxNewSynapseCount = 32,
                            permanenceIncrement = 0.1,
                            permanenceDecrement = 0.1,
                            activationThreshold = 13,
                            )
        tm.compute(inputColumns[0], learn = True)
        for y in range(3):
            for x in range(1, 5):
                leds[x].on(0.14)
            sleep(0.25)
        mode = 1
    elif mode == 1:
        if state:
            leds[index].on()
            speaker.play(tones[index])
            tm.compute(inputColumns[index], learn = True)
            if len(tm.getActiveCells()) > 40:
                bursting = True
        else:
            leds[index].off()
            speaker.stop()
            if bursting:
                bursting = False
                mode = 0
                sleep(1)
                unfold()

buttonPins = [10, 9, 11, 5, 6]
buttons = []
for x in range(5):
    buttons.append(Button(x, buttonPins[x], buttoncb))

tm.reset()
tm.compute(inputColumns[0], learn = True)
for y in range(3):
    for x in range(1, 5):
        leds[x].on(0.14)
    sleep(0.25)
mode = 1

try:
    while True:
        pass
finally:
    GPIO.cleanup()

