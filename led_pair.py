import RPi.GPIO as GPIO


# Class to handle an LED (emitter) and photoresistor (reciever) pair
class LEDPair:

    def __init__(self, reciever_pin, reciever_vcc_pin):
        self.PIN_RECIEVER = reciever_pin # GPIO input pin for photoresistor
        self.PIN_VCC_RECIEVER = reciever_vcc_pin # GPIO output to supply voltage to photoresistor input


    # Turn on the photoresistor
    def on(self):
        GPIO.output(self.PIN_VCC_RECIEVER, GPIO.HIGH)


    # Turn off the photoresistor
    def off(self):
        GPIO.output(self.PIN_VCC_RECIEVER, GPIO.LOW)


    # Check the reciever is no longer sensing light - GPIO input will read HIGH or "True"
    def reciever_covered(self):
        return GPIO.input(self.PIN_RECIEVER)
