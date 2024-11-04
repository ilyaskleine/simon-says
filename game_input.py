import json
import pygame

class SensorField:
    def __init__(self):
        self.trigger_value = 5 # set active, if one median is lower (DISTANCE FROM SENSOR)
        self.active = False

    def update(self, values):
        print(values)
        for value in values:
            if value < self.trigger_value:
                self.active = True
                return
            self.active = False

# Class for handling input from keyboard / sensors 
class GameInput:
    def __init__(self, sharedDataObject):
        self.sharedDataObject = sharedDataObject
        self.keyboardMode = False
        
        self.sensor_l = SensorField()
        self.sensor_r = SensorField()
        self.sensor_f = SensorField()
        self.sensor_b = SensorField()
    
    def get_pressed(self):
        return pygame.key.get_pressed()
    
    def update_sensors(self):
        if not self.keyboardMode:
            # Gets all four distances and updates the SensorField objects
            self.sensor_l.update(self.sharedDataObject.getLeft())
            self.sensor_r.update(self.sharedDataObject.getRight())
            self.sensor_f.update(self.sharedDataObject.getFront())
            self.sensor_b.update(self.sharedDataObject.getBack())

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
            self.update_sensors()
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
                return self.sharedDataObject.getLeft()
            except json.decoder.JSONDecodeError:
                print("Decode-Error (debug)");
