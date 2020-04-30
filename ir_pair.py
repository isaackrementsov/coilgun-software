import RPi.GPIO as GPIO


# Class to handle an IR LED (emitter) and phototransistor (reciever) pair
class IRPair:

    def __init__(self, emitter_pin, reciever_pin):
        self.PIN_EMITTER = emitter_pin # GPIO output connection for LED
        self.PIN_RECIEVER = reciever_pin # GPIO input pin for phototransistor


    # Turn on the emitter LED
    def on(self):
        GPIO.output(self.PIN_EMITTER, GPIO.HIGH)


    # Turn off the emitter LED
    def off(self):
        GPIO.output(self.PIN_EMITTER, GPIO.LOW)


    # Check the reciever is no longer sensing light - GPIO input will read HIGH or "True"
    def reciever_covered(self):
        return GPIO.input(self.PIN_RECIEVER)
