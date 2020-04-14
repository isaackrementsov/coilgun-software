import time
import RPi.GPIO as GPIO


# Class to control inductor coils for coilgun
class Coils:

    # Initialize with the GPIO pins connected to the coil 1 and 2 circuit loops
    def __init__(self, pin_coil_1, pin_coil_2, pulse_time_1, pulse_time_2):
        self.PINS = [pin_coil_1, pin_coil_2] # An array storing the pins of both coils
        self.PULSE_TIMES = [pulse_time_1, pulse_time_2] # Set a pulse time - this must be low enough to prevent a restoring force on the projectile and prevent the resistors from overheating


    # Send a very brief HIGH pulse to send current through a coil and generate a magnetic field
    def pulse_coil(index):
        # Select one of the two coils to pulse
        CURRENT_PIN = self.PINS[index]

        # Send a HIGH signal
        GPIO.output(CURRENT_PIN, GPIO.HIGH)

        # Wait for a specified amount of time
        time.sleep(self.PULSE_TIME)

        # Send a LOW signal to deactivate the coil
        GPIO.output(CURRENT_PIN, GPIO.LOW)
