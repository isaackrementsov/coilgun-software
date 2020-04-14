from random import randint
import time

# Class to interface with the ultrasonic distance sensor
class DistanceSensor:

    # Save necessary parameters on class initialization
    def __init__(self, echo, trig):
        self.PIN_ECHO = echo # GPIO pin to connect to echo sensor
        self.PIN_TRIG = trig # GPIO pin to connect to frequency pulse trigger


    # Get a reading from the distance sensor
    def get_reading(self):
        time.sleep(1)
        return randint(0, 100)/1000 + 0.1
