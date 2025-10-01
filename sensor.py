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

RECEIVER_PIN1 = 18
RECEIVER_PIN2 = 18
RECEIVER_PIN3 = 18
RECEIVER_PIN4 = 18

class Sensor:
    def __init__(self, tag, sharedDataObject):
        self.tag = tag
        self.sharedDataObject = sharedDataObject
        self.median_size = 3 # how many values the median should use
        self.values_median = [] # stores ten values for calculating one median

    def update(self, value):
        if value == None: return
        if self.tag == "l":
            self.sharedDataObject.left = value
        elif self.tag == "r":
            self.sharedDataObject.right = value
        elif self.tag == "f":
            self.sharedDataObject.front = value
        elif self.tag == "b":
            self.sharedDataObject.back = value
        return
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
    def __init__(self, sharedDataObject):
        self.ready = False
        self.sharedDataObject = sharedDataObject
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(RECEIVER_PIN1, GPIO.IN)
        GPIO.setup(RECEIVER_PIN2, GPIO.IN)
        GPIO.setup(RECEIVER_PIN3, GPIO.IN)
        GPIO.setup(RECEIVER_PIN4, GPIO.IN)

        GPIO.add_event_detect(RECEIVER_PIN1, GPIO.RISING, callback=self.sensorCallback, bouncetime=200)
        GPIO.add_event_detect(RECEIVER_PIN2, GPIO.RISING, callback=self.sensorCallback, bouncetime=200)
        GPIO.add_event_detect(RECEIVER_PIN3, GPIO.RISING, callback=self.sensorCallback, bouncetime=200)
        GPIO.add_event_detect(RECEIVER_PIN4, GPIO.RISING, callback=self.sensorCallback, bouncetime=200)
        print("Waiting for sensors to settle")
        time.sleep(2)
        self.ready = True
        self.active = None

    def sensorCallback(self, channel):
        if channel == 18:
            self.sharedDataObject.left = GPIO.iput(channel)
        elif channel == 18:
            self.sharedDataObject.right = GPIO.iput(channel)
        elif channel == 18:
            self.sharedDataObject.front = GPIO.iput(channel)
        elif channel == 18:
            self.sharedDataObject.back = GPIO.iput(channel)

    def initPins(self, trg, ech):
        GPIO.setup(trg, GPIO.OUT)
        GPIO.setup(ech, GPIO.IN)
        GPIO.output(trg, GPIO.LOW)

    def getDistance(self, trg, ech):
        # print(f"Getting distance of {trg}")
        GPIO.output(trg, GPIO.HIGH)

        time.sleep(0.00001)

        GPIO.output(trg, GPIO.LOW)

        pulse_start_time = time.time()
        while GPIO.input(ech)==0:
            pulse_start_time = time.time()
        while GPIO.input(ech)==1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        # print(f"Finished distance of {trg}")
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
        # leftSensor = Sensor("l", sharedDataObject)
        # rightSensor = Sensor("r", sharedDataObject)
        # frontSensor = Sensor("f", sharedDataObject)
        # backSensor = Sensor("b", sharedDataObject)
        pass


class SensorThread:
    def __init__(self, sharedDataObject):
        self.controller = None

    def run(self, sharedDataObject):
        self.controller = SensorController(sharedDataObject)