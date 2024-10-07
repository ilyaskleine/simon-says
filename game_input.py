import json
import pygame
import statistics

from input_debug import SensorData

class SensorField:
    def __init__(self):
        self.trigger_value = 5 # set active, if one median is lower (DISTANCE FROM SENSOR)
        self.median_size = 10 # how many values the median should use
        self.values_median = [] # stores ten values for calculating one median
        self.values = [] # stores three calculated medians to check if one triggers
        self.active = False

    def update(self, value):
        if len(self.values_median) < self.median_size: # Collecting data for median
            self.values_median.append(value)
        else: # Enough data for median: 
            if len(self.values) < 3: # Collect three medians
                median = statistics.median(self.values_median)
                self.values_median = []
                self.values.append(median)
            else: # Check if one of them is below the trigger
                print(self.values)
                for value in self.values:
                    if value < self.trigger_value:
                        self.active = True
                        self.values = []
                        return
                self.active = False
                self.values = []

# Class for handling input from keyboard / sensors 
class GameInput:
    def __init__(self, keyboard):
        self.keyboardMode = keyboard
        if not self.keyboardMode:
            self.sensorInstance = SensorData()
        
        self.sensor_l = SensorField()
        self.sensor_r = SensorField()
        self.sensor_f = SensorField()
        self.sensor_b = SensorField()
    
    def get_pressed(self):
        return pygame.key.get_pressed()
    
    def background_update_sensors(self):
        if not self.keyboardMode:
            # Gets all four distances and updates the SensorField objects
            data = self.sensorInstance.getAll()
            self.sensor_l.update(data["l"])
            self.sensor_r.update(data["r"])
            self.sensor_f.update(data["f"])
            self.sensor_b.update(data["b"])

    def check(self):
        if self.keyboardMode:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                return "up"
            if keys[pygame.K_DOWN]:
                return "down"
            if keys[pygame.K_LEFT]:
                return "left"
            if keys[pygame.K_RIGHT]:
                return "right"
        else:
            # Convert active fields to keyboard-like input
            if self.sensor_l.active:
                return "left"
            if self.sensor_r.active:
                return "right"
            if self.sensor_f.active:
                return "up"
            if self.sensor_b.active:
                return "down"
            
    def debug(self):
        if not self.keyboardMode:
            try:
                return self.sensorInstance.getAll()
            except json.decoder.JSONDecodeError:
                print("Decode-Error (debug)");
