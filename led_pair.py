import RPi.GPIO as GPIO


# Class to handle an LED (emitter) and photoresistor (reciever) pair
class LEDPair:

    def __init__(self, reciever_pin):
        self.PIN_RECIEVER = reciever_pin # GPIO input pin for photoresistor


    # Turn on the photoresistor
    def on(self):
        GPIO.output(self.PIN_RECIEVER, GPIO.HIGH)


    # Turn off the photoresistor
    def off(self):
        GPIO.output(self.PIN_RECIEVER, GPIO.LOW)


    # Check the reciever is no longer sensing light - GPIO input will read HIGH or "True"
    def reciever_covered(self):
        return GPIO.input(self.PIN_RECIEVER)
