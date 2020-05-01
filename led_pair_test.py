# Code to test infrared emitter/reciever pairs

import RPi.GPIO as GPIO
from led_pair import LEDPair

# Pin to connect to reciever (input) and reciever VCC (output)
PIN_RECIEVER = 22
PIN_VCC_RECIEVER = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(PIN_RECIEVER, GPIO.IN)
GPIO.setup(PIN_VCC_RECIEVER, GPIO.OUT)

# Initialize a new LED pair
pair = LEDPair(PIN_RECIEVER, PIN_VCC_RECIEVER)

try:
    # Turn on reciever
    pair.on()

    i = 0
    # Continuously output reciever data
    while True:
        if pair.reciever_covered():
            i += 1
            print('Input #' + str(i))

except KeyboardInterrupt:
    # Clean exit on interrupt
    pair.off()
    GPIO.cleanup()
    exit()
