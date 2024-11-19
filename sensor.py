import RPi.GPIO as GPIO
import statistics
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

class Sensor:
    def __init__(self, tag, sharedDataObject):
        self.tag = tag
        self.sharedDataObject = sharedDataObject
        self.median_size = 3 # how many values the median should use
        self.values_median = [] # stores ten values for calculating one median

    def update(self, value):
        if value == None: return;
        if len(self.values_median) < self.median_size: # Collecting data for median
            self.values_median.append(value)
        else: # Enough data for median: 
            median = statistics.median(self.values_median)
            self.values_median = []
            if self.tag == "l":
                self.sharedDataObject.left = median
            elif self.tag == "r":
                self.sharedDataObject.right = median
            elif self.tag == "f":
                self.sharedDataObject.front = median
            elif self.tag == "b":
                self.sharedDataObject.back = median


class SensorController:
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

    def run(self, sharedDataObject):
        leftSensor = Sensor("l", sharedDataObject)
        rightSensor = Sensor("r", sharedDataObject)
        frontSensor = Sensor("f", sharedDataObject)
        backSensor = Sensor("b", sharedDataObject)
        while True:
            if self.ready:
                leftSensor.update(self.getDistance(L_TRIGGER, L_ECHO))
                rightSensor.update(self.getDistance(R_TRIGGER, R_ECHO))
                frontSensor.update(self.getDistance(B_TRIGGER, B_ECHO))
                backSensor.update(self.getDistance(F_TRIGGER, F_ECHO))








    
