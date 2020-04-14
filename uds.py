import time


# Class to interface with the ultrasonic distance sensor
class DistanceSensor:

    # Save necessary parameters on class initialization
    def __init__(self, echo, trig):
        self.PIN_ECHO = echo # GPIO pin to connect to echo sensor
        self.PIN_TRIG = trig # GPIO pin to connect to frequency pulse trigger


    # Get a reading from the distance sensor
    def get_reading(self):
        # Code below is based on Gaven MacDonald's video: https://www.youtube.com/watch?v=xACy8l3LsXI

        PIN_TRIG = self.PIN_TRIG
        PIN_ECHO = self.PIN_ECHO

        # Give the sensor time to settle
        time.sleep(0.1)

        # Use the trigger pin to emit a 10 microsecond ultrasonic pulse
        GPIO.output(PIN_TRIG, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIG, GPIO.LOW)

        # Wait for the echo pin to send a HIGH signal, meaning the pulse signal has been detected
        while GPIO.input(PIN_ECHO) == GPIO.LOW:
            pass

        start = time.time()

        # Wait for the echo pin to finish the HIGH singal, meaning the pulse signal has ended
        while GPIO.input(PIN_TRIG) == GPIO.HIGH:
            pass

        end = time.time()

        # Use the speed of sound to find how far the signal travelled to last for the time elapsed (eq 7)
        time_elapsed = start - end
        distance_reading = 171.5*time_elapsed
