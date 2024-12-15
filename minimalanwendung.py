#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
import pygame
import statistics

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
 
#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#GPIO Pins zuweisen
GPIO_TRIGGER = 23
GPIO_ECHO = 24
 
#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#GPIO Pins zuweisen
GPIO_TRIGGER = 6
GPIO_ECHO = 13
 
#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#GPIO Pins zuweisen
GPIO_TRIGGER = 16
GPIO_ECHO = 20
 
#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#GPIO Pins zuweisen
GPIO_TRIGGER = 19
GPIO_ECHO = 26
 
#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distanz():
    alleDistanzen = []
    n = 0
    while n <= 3:
        # setze Trigger auf HIGH
        GPIO.output(GPIO_TRIGGER, True)
    
        # setze Trigger nach 0.01ms aus LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
    
        StartZeit = time.time()
        StopZeit = time.time()
    
        # speichere Startzeit
        while GPIO.input(GPIO_ECHO) == 0:
            StartZeit = time.time()
    
        # speichere Ankunftszeit
        while GPIO.input(GPIO_ECHO) == 1:
            StopZeit = time.time()
    
        # Zeit Differenz zwischen Start und Ankunft
        TimeElapsed = StopZeit - StartZeit
        # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
        # und durch 2 teilen, da hin und zurueck
        distanz = (TimeElapsed * 34300) / 2
        alleDistanzen.append(distanz)
        n += 1
        time.sleep(0.001)
    return statistics.median(alleDistanzen)
 
if __name__ == '__main__':
    try:
        pygame.init()
        screen = pygame.display.set_mode((1000, 720))
        clock = pygame.time.Clock() 
        running = True
        centerX = screen.get_width() / 2
        centerY = screen.get_height() / 2
        fieldWidth = 200
        threshold = 60
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((255, 255, 255))
            GPIO_TRIGGER = 23
            GPIO_ECHO = 24
            abstand = distanz()
            print ("Gemessene Entfernung (F) = %.1f cm" % abstand)
            if (abstand < threshold):
                pygame.draw.rect(screen, red, pygame.Rect(centerX - (fieldWidth / 2), 0, fieldWidth, fieldWidth))
            time.sleep(0.01)
            GPIO_TRIGGER = 6
            GPIO_ECHO = 13
            abstand = distanz()
            print ("Gemessene Entfernung (L) = %.1f cm" % abstand)
            if (abstand < threshold):
                pygame.draw.rect(screen, green, pygame.Rect(0, centerY - (fieldWidth / 2), fieldWidth, fieldWidth))
            time.sleep(0.01)
            GPIO_TRIGGER = 16
            GPIO_ECHO = 20
            abstand = distanz()
            print ("Gemessene Entfernung (B) = %.1f cm" % abstand)
            if (abstand < threshold):
                pygame.draw.rect(screen, blue, pygame.Rect(centerX - (fieldWidth / 2), centerY*2 - fieldWidth, fieldWidth, fieldWidth))
            time.sleep(0.01)
            GPIO_TRIGGER = 19
            GPIO_ECHO = 26
            abstand = distanz()
            print ("Gemessene Entfernung (R) = %.1f cm" % abstand)
            if (abstand < threshold):
                pygame.draw.rect(screen, yellow, pygame.Rect(centerX*2 - fieldWidth, centerY - (fieldWidth / 2), fieldWidth, fieldWidth))
            time.sleep(0.01)
            pygame.display.flip()
            clock.tick(30)
 
        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()

    except Exception as error:
        print(error)