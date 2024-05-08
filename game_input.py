import json
import pygame

# Klasse für Verarbeitung von Tastatur / Sensoren
class GameInput:
    def __init__(self, keyboard):
        self.keyboardMode = keyboard
        self.threshold = 15
    
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
            self.jsonToInput()

    def jsonToInput(self):
        with open('distances.json') as file:
            data = json.load(file)
            l = data["l"]
            r = data["r"]
            f = data["f"]
            b = data["b"]
            if l > self.threshold:
                return "up"