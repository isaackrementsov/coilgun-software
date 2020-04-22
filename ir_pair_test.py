# Code to test infrared emitter/reciever pairs

import RPi.GPIO as GPIO
from ir_pair import IRPair

# Pin to connect to emitter (output) and reciever (input)
PIN_EMITTER = 23
PIN_RECIEVER = 18

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(PIN_EMITTER, GPIO.OUTPUT)
GPIO.setup(PIN_RECIEVER, GPIO.INPUT)

# Initialize a new IR pair
pair = IRPair(PIN_EMITTER, PIN_RECIEVER)

try:
    # Turn on emitter
    pair.on()
    
    # Continuously output reciever data
    while True:
        print(pair.reciever_covered())

except KeyboardInterrupt:
    pair.off()
    GPIO.cleanup()
    exit()
