import pygame
import random

from sensor_debug import SensorThread
from data_classes import SensorData, LogicData
from thread_logic import LogicThread
import time
from threading import Thread

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

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
            
class User:
    def __init__(self):
        self.score = 0;

    def scoreUp(self):
        self.score += 1

# Grafikobjekt: Box mit verschiedenen Farben     

class Field:
    def __init__(self, side, screen, sharedGameState):
        self.screen = screen
        self.side = side
        self.sharedGameState = sharedGameState
        # Computed values
        self.posX = screen.get_width() / 2 - side / 2
        self.posY = screen.get_height() / 2 - side / 2
        cornerWidth = side / 2
        # Config 
        self.colorsToKey = {"red": "right", "yellow": "down", "blue": "up", "green": "left"}
        self.color = "black"
        self.blinkTime = 1000
        # (Child) Objects
        self.topLeft = Corner(self.screen, self.posX, self.posY, cornerWidth, blue)
        self.topRight = Corner(self.screen, self.posX + cornerWidth, self.posY, cornerWidth, red)
        self.bottomLeft = Corner(self.screen, self.posX, self.posY  + cornerWidth, cornerWidth, green)
        self.bottomRight = Corner(self.screen, self.posX + cornerWidth, self.posY + cornerWidth, cornerWidth, yellow)
        # Algoritmic Variables
        self.query = []
        self.queryLength = 1
        self.setRandomQuery()
        self.index = 0
        self.round = 0
        self.activationTick = pygame.time.get_ticks()
        self.guess = None
        self.guessIndex = 0
        self.cooldown = pygame.time.get_ticks()
        self.score = 0

    def draw(self):
        self.act()
        # Feld + Subdivs
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.posX, self.posY, self.side, self.side))
        self.topLeft.draw()
        self.topRight.draw()
        self.bottomLeft.draw()
        self.bottomRight.draw()
        # Score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

    def act(self):
        now = pygame.time.get_ticks()
        if len(self.query) == self.index: # Wenn Alle gezeigt wurden ...
            #print("All were shown")
            if now - self.cooldown >= self.blinkTime:
                if now - self.activationTick >= self.blinkTime:
                    self.disableAllChild()
                print("Checking...")
                self.checkInput()
                if len(self.query) == self.guessIndex: # Wenn fertig geratem
                    self.queryLength += 1
                    self.setRandomQuery()
                    self.blinkTime = self.blinkTime * 0.95
                    self.round += 1
                    self.index = 0
                    self.guessIndex = 0
                    self.activationTick = pygame.time.get_ticks()
                    return
                if self.query[self.guessIndex] == self.guess:
                    self.guess = None
                    print("True")
                    self.guessIndex += 1
                    self.score += 1
                    self.cooldown = pygame.time.get_ticks()
                elif self.guess:
                    print("False")
                    self.guess = None
                    self.cooldown = pygame.time.get_ticks()
                    # => Implement Loosing Logic

                self.guess = None
            else:
                #print(self.guess)
                pass
                #print(self.query[self.guessIndex] == self.guess)
            return
        if now - self.activationTick >= self.blinkTime: # Wenn das akt. Feld lang genug geleuchtet hat...
            # wechsle zum nächsten Feld
            current = self.query[self.index]
            print(current)
            self.disableAllChild()
            if current == "blue":
                self.topLeft.activate()
            elif current == "red":
                self.topRight.activate()
            elif current == "green":
                self.bottomLeft.activate()
            elif current == "yellow":
                self.bottomRight.activate()
            self.index += 1
            self.activationTick = pygame.time.get_ticks()

    def disableAllChild(self):
        self.topLeft.deactivate()
        self.topRight.deactivate()
        self.bottomLeft.deactivate()
        self.bottomRight.deactivate()
            

    def checkInput(self):
        input = self.sharedGameState.activeField
        if input:
            if input == "up":
                self.guess = "blue"
                self.topLeft.activate()
            elif input == "right":
                self.guess = "red"
                self.topRight.activate()
            elif input == "left":
                self.guess = "green"
                self.bottomLeft.activate()
            elif input == "down":
                self.guess = "yellow"
                self.bottomRight.activate()

    def setRandomQuery(self):
        result = []
        for i in range(self.queryLength):
            pool = list(self.colorsToKey.keys())
            if i > 0:
                pool.remove(result[i - 1])
            choice = random.choice(pool)
            result.append(choice)
        self.query = result

            
class Corner:
    def __init__(self, screen, x, y, width, color):
        self.screen = screen
        self.width = width
        self.posX = x
        self.posY = y
        self.active = False
        self.color = color
        self.blinkTime = 1000
        self.activationTick = pygame.time.get_ticks()

    def draw(self):
        if self.active:
            pygame.draw.rect(self.screen, self.color, pygame.Rect(self.posX, self.posY, self.width, self.width))
            # now = pygame.time.get_ticks()
            # if now - self.activationTick >= self.blinkTime:
            #     self.active = False

    def setColor(self, color):
        if color == "red":
            self.color = red
        elif color == "blue":
            self.color == blue
        elif color == "green":
            self.color = green
        elif color == "yellow":
            self.color == yellow

    def activate(self):
        self.active = True
        # self.activationTick = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False

        
class Game:
    def __init__(self, debug, sharedGameState):
        # Pygame Setup
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((1000, 720));
        pygame.display.set_caption("Farbfelder")
        self.clock = pygame.time.Clock() 
        self.running = True # Game Loop an aus 
        self.dt = 0 # Für alles was sich bewegen würde
        self.smallBoxWidth = 45;
        self.smallBoxDistance = 250;

        self.gameInput = GameInput(True)
        self.user = User()

        # Erstellung der Grafikobjekte
        self.mainBox = Field(400, self.screen, sharedGameState)
        
    def gameLoop(self, sharedGameState):
        # --- Game-Loop ---
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Hintergrund
            self.screen.fill("white")
            self.mainBox.draw()

            pygame.display.flip()

            # Setzt FPS
            dt = self.clock.tick(30) / 1000 

        pygame.quit()

sharedDataObject = SensorData()
sharedGameState = LogicData()
sensorThread = Thread(target=SensorThread().run, args=(sharedDataObject,))
sensorThread.start()
logicThread = Thread(target=LogicThread(sharedDataObject, sharedGameState).run, args=())
logicThread.start()
game = Game(debug=True, sharedGameState=sharedGameState)
game.gameLoop(sharedGameState)