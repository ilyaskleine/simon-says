import RPi.GPIO as GPIO
import json
import time


run = True

L_TRIGGER = 6
L_ECHO = 13
R_TRIGGER = 19
R_ECHO = 26
B_TRIGGER = 16
B_ECHO = 20
F_TRIGGER = 23
F_ECHO = 24

class SensorData:
    def __init__(self):
        self.ready = False
        GPIO.setmode(GPIO.BCM)
        self.initPins(L_TRIGGER, L_ECHO)
        self.initPins(R_TRIGGER, R_ECHO)
        self.initPins(B_TRIGGER, B_ECHO)
        self.initPins(F_TRIGGER, F_ECHO)
        print("Waiting for sensors to settle")
        time.sleep(2)
        self.ready = True

    def initPins(self, trg, ech):
        GPIO.setup(trg, GPIO.OUT)
        GPIO.setup(ech, GPIO.IN)
        GPIO.output(trg, GPIO.LOW)

    def getDistance(self, trg, ech):
        GPIO.output(trg, GPIO.HIGH)

        time.sleep(0.00001)

        GPIO.output(trg, GPIO.LOW)

        while GPIO.input(ech)==0:
            pulse_start_time = time.time()
        while GPIO.input(ech)==1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        print("Distance:",distance,"cm")
        return distance
    
    def getAll(self):
        if not self.ready:
            return {"l": 0, "r": 0, "b": 0, "f": 0}
        distances = {
            "l": self.getDistance(L_TRIGGER, L_ECHO),
            "r": self.getDistance(R_TRIGGER, R_ECHO),
            "b": self.getDistance(B_TRIGGER, B_ECHO),
            "f": self.getDistance(F_TRIGGER, F_ECHO)
        }
        return distances

    def cleanUp(self):
        GPIO.cleanup()





    
