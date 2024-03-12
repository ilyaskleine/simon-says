import pygame
import random
import time

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
        else:
            with open("herald.lag", "r") as inputfile:
                print("File: " + inputfile.readline())
                #print(time.time())
            
            
class User:
    def __init__(self):
        self.score = 0;

    def scoreUp(self):
        self.score += 1

# Grafikobjekt: Box mit verschiedenen Farben     

class Field:
    def __init__(self, side):
        global screen
        self.side = side
        self.posX = screen.get_width() / 2 - side / 2
        self.posY = screen.get_height() / 2 - side / 2
        self.colorsToKey = {"red": "up", "violet": "down", "blue": "left", "green": "right"}
        #self.color = random.choice(list(self.colorsToKey.keys()))
        self.color = "black"
        cornerWidth = side / 2

        self.topLeft = Corner(self.posX, self.posY, cornerWidth, "blue")
        self.topRight = Corner(self.posX + cornerWidth, self.posY, cornerWidth, "red")
        self.bottomLeft = Corner(self.posX, self.posY  + cornerWidth, cornerWidth, "green")
        self.bottomRight = Corner(self.posX + cornerWidth, self.posY + cornerWidth, cornerWidth, "violet")

        self.query = []
        self.index = 0
        self.round = 0
        self.blinkTime = 900
        self.activationTick = pygame.time.get_ticks()
        self.setRandomQuery(5)


    def draw(self):
        global screen
        self.act()
        pygame.draw.rect(screen, self.color, pygame.Rect(self.posX, self.posY, self.side, self.side))
        self.topLeft.draw()
        self.topRight.draw()
        self.bottomLeft.draw()
        self.bottomRight.draw()

    def act(self):
        if len(self.query) == self.index:
            # Finished Show-Off Phase
            return
        now = pygame.time.get_ticks()
        if now - self.activationTick >= self.blinkTime:
            current = self.query[self.index]
            print(current)
            self.disableAllChild()
            if current == "red":
                self.topLeft.activate()
            elif current == "green":
                self.topRight.activate()
            elif current == "blue":
                self.bottomLeft.activate()
            elif current == "violet":
                self.bottomRight.activate()
            self.index += 1
            self.activationTick = pygame.time.get_ticks()

    def disableAllChild(self):
        self.topLeft.deactivate()
        self.topRight.deactivate()
        self.bottomLeft.deactivate()
        self.bottomRight.deactivate()
            

    def checkInput(self, input):
        if input and len(self.query) == self.index:
            if input == "up":
                self.index = 0
                self.setRandomQuery(5)
            elif input == "right":
                self.topRight.activate()
            elif input == "left":
                self.bottomLeft.activate()
            elif input == "down":
                self.bottomRight.activate()

    def setRandomQuery(self, length):
        result = []
        for i in range(length):
            pool = list(self.colorsToKey.keys())
            if i > 0:
                pool.remove(result[i - 1])
            choice = random.choice(pool)
            result.append(choice)
        self.query = result

            
class Corner:
    def __init__(self, x, y, width, color):
        self.width = width
        self.posX = x
        self.posY = y
        self.active = False
        self.color = color
        self.blinkTime = 1000
        self.activationTick = pygame.time.get_ticks()

    def draw(self):
        if self.active:
            pygame.draw.rect(screen, self.color, pygame.Rect(self.posX, self.posY, self.width, self.width))
            # now = pygame.time.get_ticks()
            # if now - self.activationTick >= self.blinkTime:
            #     self.active = False

    def activate(self):
        self.active = True
        # self.activationTick = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False

        


# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((1000, 720));
pygame.display.set_caption("Farbfelder")
clock = pygame.time.Clock() 
running = True # Game Loop an aus 
dt = 0 # Für alles was sich bewegen würde
smallBoxWidth = 45;
smallBoxDistance = 250;

gameInput = GameInput(False)
user = User()

# Erstellung der Grafikobjekte
mainBox = Field(400)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Hintergrund
    screen.fill("white")
    # Farbkästchen an den Seiten
    #if user.score <= 5:
    #    pygame.draw.rect(screen, "red", pygame.Rect(screen.get_width() / 2 - smallBoxWidth / 2, (screen.get_height() / 2 - smallBoxWidth / 2) - smallBoxDistance, smallBoxWidth, smallBoxWidth))
    #    pygame.draw.rect(screen, "violet", pygame.Rect(screen.get_width() / 2 - smallBoxWidth / 2, (screen.get_height() / 2 - smallBoxWidth / 2) + smallBoxDistance, smallBoxWidth, smallBoxWidth))
    #    pygame.draw.rect(screen, "blue", pygame.Rect((screen.get_width() / 2 - smallBoxWidth / 2) - smallBoxDistance, screen.get_height() / 2 - smallBoxWidth / 2, smallBoxWidth, smallBoxWidth))
    #    pygame.draw.rect(screen, "green", pygame.Rect((screen.get_width() / 2 - smallBoxWidth / 2) + smallBoxDistance, screen.get_height() / 2 - smallBoxWidth / 2, smallBoxWidth, smallBoxWidth))

    mainBox.draw()

    key = gameInput.check()
    if mainBox.checkInput(key):
        user.scoreUp()
        print(user.score)
        #mainBox.randomColor()

    pygame.display.flip()

    # Setzt FPS
    dt = clock.tick(30) / 1000 

pygame.quit()