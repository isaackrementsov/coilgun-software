from random import randint
import numpy as np
import time


# Class to interface with the ultrasonic distance sensor
class DistanceSensor:

    # Save necessary parameters on class initialization
    def __init__(self, echo, trig):
        self.PIN_ECHO = echo # GPIO pin to connect to echo sensor
        self.PIN_TRIG = trig # GPIO pin to connect to frequency pulse trigger
        self.t = 0


    # Get a reading from the distance sensor
    def get_reading(self):
        time.sleep(0.1)
        self.t += 0.1
        return 0.1*np.sin(0.1*self.t) + 0.1
