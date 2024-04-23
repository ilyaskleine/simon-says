import pygame

# Klasse für Verarbeitung von Tastatur / Sensoren
class GameInput:
    def __init__(self, keyboard):
        self.keyboardMode = keyboard
    
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