# Code to test infrared emitter/reciever pairs

import RPi.GPIO as GPIO
from ir_pair import IRPair

# Pin to connect to emitter (output) and reciever (input)
PIN_EMITTER = 23
PIN_RECIEVER = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(PIN_EMITTER, GPIO.OUT)
GPIO.setup(PIN_RECIEVER, GPIO.IN)

# Initialize a new IR pair
pair = IRPair(PIN_EMITTER, PIN_RECIEVER)

try:
    # Turn on emitter
    pair.on()

    i = 0
    # Continuously output reciever data
    while True:
        if GPIO.input(PIN_RECIEVER):
            i += 1
            print('Input #' + str(i))

except KeyboardInterrupt:
    pair.off()
    GPIO.cleanup()
    exit()
