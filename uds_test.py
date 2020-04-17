# Code to test distance sensor circuit

import RPi.GPIO as GPIO
import numpy as np
from uds import DistanceSensor

# Pins to connect to echo (input) and trigger (output)
PIN_TRIG = 24
PIN_ECHO = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(PIN_TRIG, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)


# Initialize a new distance sensor
distance_sensor = DistanceSensor(PIN_ECHO, PIN_TRIG)

try:
    # Continuously output data
    while True:
        # Print detected distance in cm
        print(100*np.round(distance_sensor.get_reading(), 2))

except KeyboardInterrupt:
    GPIO.cleanup()
    exit()
        
