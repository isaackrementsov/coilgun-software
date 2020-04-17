# Code to test distance sensor circuit

import RPi.GPIO as GPIO
from uds import DistanceSensor

# Pins to connect to echo (input) and trigger (output)
PIN_TRIG = 18
PIN_ECHO = 23

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN_TRIG, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)


# Initialize a new distance sensor and print a distance reading

distance_sensor = DistanceSensor(PIN_ECHO, PIN_TRIG)

print(distance_sensor.get_reading())
