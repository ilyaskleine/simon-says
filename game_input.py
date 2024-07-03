import json
import pygame
import statistics

from input_debug import SensorData

# Klasse für Verarbeitung von Tastatur / Sensoren
class GameInput:
    def __init__(self, keyboard):
        self.keyboardMode = keyboard
        if not self.keyboardMode:
            self.sensorInstance = SensorData()
        self.threshold = 15
        self.releaseThreshold = 50
        self.lockL = False
        self.lockR = False
        self.lockF = False
        self.lockB = False

        self.meanCount = 0
        self.meanDataL = []
        self.meanDataR = []
        self.meanDataF = []
        self.meanDataB = []

        self.DataL = []
        self.DataR = []
        self.DataF = []
        self.DataB = []
    
    def get_pressed(self):
        return pygame.key.get_pressed()

    def check(self):
        if self.keyboardMode:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                return "up"
            if keys[pygame.K_s]:
                return "down"
            if keys[pygame.K_a]:
                return "left"
            if keys[pygame.K_w]:
                return "right"
        else:
            return self.jsonToInput()

    def jsonToInput(self):
        try:
                data = self.sensorInstance.getAll()
                l = data["l"]
                r = data["r"]
                f = data["f"]
                b = data["b"]
                if self.meanCount <= 10:
                    self.meanDataL.append(l)
                    self.meanDataR.append(r)
                    self.meanDataF.append(f)
                    self.meanDataB.append(b)
                    self.meanCount += 1
                else:
                    self.meanCount = 0
                    if self.dataCount < 3:
                        self.dataL.append(statistics.median(self.meanDataL))
                        self.dataR.append(statistics.median(self.meanDataR) / 10)
                        self.dataF.append(statistics.median(self.meanDataF) / 10)
                        self.dataB.append(statistics.median(self.meanDataB) / 10)
                    else:
                        for l in self.dataL:
                            if l < self.threshold:
                                self.lockL = True
                                return "left"
                            elif self.lockL and l > self.releaseThreshold:
                                self.lockL = False
                        for r in self.dataR:
                            if r < self.threshold:
                                self.lockR = True
                                return "right"
                            elif self.lockR and r > self.releaseThreshold:
                                self.lockR = False
                        for f in self.dataF:
                            if f < self.threshold:
                                self.lockF = True
                                return "up"
                            elif self.lockF and f > self.releaseThreshold:
                                self.lockF = False
                        for b in self.dataB:
                            if b < self.threshold:
                                self.lockB = True
                                return "down"
                            elif self.lockB and b > self.releaseThreshold:
                                self.lockB = False
                    

        except json.decoder.JSONDecodeError:
            print("Decode-Error");
    
    def debug(self):
        if not self.keyboardMode:
            try:
                return self.sensorInstance.getAll()
            except json.decoder.JSONDecodeError:
                print("Decode-Error (debug)");
