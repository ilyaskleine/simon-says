import RPi.GPIO as GPIO
import time


run = True

while run:
    time.sleep(1)
    with open("herald.lag", "w") as outfile:
        outfile.write(str(time.time()))


L_TRIGGER = 6
L_ECHO = 13
R_TRIGGER = 19
R_ECHO = 26
B_TRIGGER = 16
B_ECHO = 20
F_TRIGGER = 23
F_ECHO = 24

def initPins(trg, ech):
    GPIO.setup(trg, GPIO.OUT)
    GPIO.setup(ech, GPIO.IN)
    GPIO.output(trg, GPIO.LOW)

def getDistance(trg, ech):
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

initPins(L_TRIGGER, L_ECHO)
initPins(R_TRIGGER, R_ECHO)
initPins(B_TRIGGER, B_ECHO)
initPins(F_TRIGGER, F_ECHO)

print("Waiting for sensors to settle")
time.sleep(2)

while True:
    # ... Logik mit Trigger-Distanz und schreiben in Datei
    getDistance(L_TRIGGER, L_ECHO)
    getDistance(R_TRIGGER, R_ECHO)
    getDistance(B_TRIGGER, B_ECHO)
    getDistance(F_TRIGGER, F_ECHO)

      


GPIO.cleanup()
    
