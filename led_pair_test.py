# Code to test infrared emitter/reciever pairs

import RPi.GPIO as GPIO
from led_pair import LEDPair

# Pin to connect to emitter (output) and reciever (input)
PIN_RECIEVER = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(PIN_RECIEVER, GPIO.IN)

# Initialize a new LED pair
pair = LEDPair(PIN_RECIEVER)

try:
    # Turn on reciever
    pair.on()

    i = 0
    # Continuously output reciever data
    while True:
        if GPIO.input(PIN_RECIEVER):
            i += 1
            print('Input #' + str(i))

except KeyboardInterrupt:
    # Clean exit on interrupt
    pair.off()
    GPIO.cleanup()
    exit()
