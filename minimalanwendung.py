#Bibliotheken einbinden
import RPi.GPIO as GPIO
import pygame

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
 
#GPIO Modus (BOARD / BCM)
RECEIVER_PIN1 = 18
RECEIVER_PIN2 = 18
RECEIVER_PIN3 = 18
RECEIVER_PIN4 = 18
active = None

def callback_func(channel):
    if GPIO.input(channel):
        global active
        active = channel

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RECEIVER_PIN1, GPIO.IN)
GPIO.setup(RECEIVER_PIN2, GPIO.IN)
GPIO.setup(RECEIVER_PIN3, GPIO.IN)
GPIO.setup(RECEIVER_PIN4, GPIO.IN)

GPIO.add_event_detect(RECEIVER_PIN1, GPIO.RISING, callback=callback_func, bouncetime=200)
GPIO.add_event_detect(RECEIVER_PIN2, GPIO.RISING, callback=callback_func, bouncetime=200)
GPIO.add_event_detect(RECEIVER_PIN3, GPIO.RISING, callback=callback_func, bouncetime=200)
GPIO.add_event_detect(RECEIVER_PIN4, GPIO.RISING, callback=callback_func, bouncetime=200)

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
            if active == RECEIVER_PIN1:
                pygame.draw.rect(screen, red, pygame.Rect(centerX - (fieldWidth / 2), 0, fieldWidth, fieldWidth))
            elif active == RECEIVER_PIN2:
                pygame.draw.rect(screen, green, pygame.Rect(0, centerY - (fieldWidth / 2), fieldWidth, fieldWidth))
            elif active == RECEIVER_PIN3:
                pygame.draw.rect(screen, blue, pygame.Rect(centerX - (fieldWidth / 2), centerY*2 - fieldWidth, fieldWidth, fieldWidth))
            elif active == RECEIVER_PIN4:
                pygame.draw.rect(screen, yellow, pygame.Rect(centerX*2 - fieldWidth, centerY - (fieldWidth / 2), fieldWidth, fieldWidth))
            pygame.display.flip()
            clock.tick(30)
 
        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()
        GPIO.remove_event_detect(RECEIVER_PIN1)
        GPIO.remove_event_detect(RECEIVER_PIN2)
        GPIO.remove_event_detect(RECEIVER_PIN3)
        GPIO.remove_event_detect(RECEIVER_PIN4)

    except Exception as error:
        print(error)
        GPIO.remove_event_detect(RECEIVER_PIN1)
        GPIO.remove_event_detect(RECEIVER_PIN2)
        GPIO.remove_event_detect(RECEIVER_PIN3)
        GPIO.remove_event_detect(RECEIVER_PIN4)