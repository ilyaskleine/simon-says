import pygame
import random
from game_input import GameInput
import math

pygame.mixer.init()

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
gameInput = GameInput(True)

def rot_center(image, angle, x, y):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect

def getPosForCenterCord(centerX, centerY, width):
    offset = width / 2
    return (centerX - offset, centerY - offset)

# Grafikobjekt: Box mit verschiedenen Farben     
class Field:
    def __init__(self, screen, side):
        self.screen = screen
        self.side = side
        # Computed values
        self.posX = screen.get_width() / 2 - side / 2
        self.posY = screen.get_height() / 2 - side / 2
        cornerWidth = int(side / 2);
        # Config 
        self.colorsToKey = {"red": "right", "yellow": "down", "blue": "up", "green": "left"}
        self.color = (0, 0, 0)
        self.blinkTime = 1000
        # (Child) Objects
        self.topLeft = Corner(self.screen, cornerWidth, "blue", 2)
        self.topRight = Corner(self.screen, cornerWidth, "red", 1)
        self.bottomLeft = Corner(self.screen, cornerWidth, "green", 3)
        self.bottomRight = Corner(self.screen, cornerWidth, "yellow", 4)
        # Algoritmic Variables
        self.reset()
        self.clickSound = pygame.mixer.Sound('sounds/rollover1.wav') # alt: switch2.wav
        self.activeSound = pygame.mixer.Sound('sounds/rollover1.wav')
        self.gameOverSound = pygame.mixer.Sound('sounds/Downer01.wav')
        self.roundFinishSound = pygame.mixer.Sound('sounds/Coin01.wav')

    def draw(self):
        self.act()
        # Feld + Subdivs
        # pygame.draw.rect(self.screen, self.color, pygame.Rect(self.posX, self.posY, self.side, self.side))
        self.topLeft.draw()
        self.topRight.draw()
        self.bottomLeft.draw()
        self.bottomRight.draw()
        # Score
        font = pygame.font.Font('fonts/jersey.ttf', 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        round_text = font.render(f'Runde {self.round + 1}', True, (255, 255, 255))
        self.screen.blit(round_text, (self.screen.get_width() - 130, 10))
        # return: Szenen die als nächstes folgen soll
        if self.gameOver:
            pygame.mixer.Sound.play(self.gameOverSound)
            return "gameOver"
        else:
            return "game"

    def act(self):
        global scene
        now = pygame.time.get_ticks()
        if len(self.query) == self.index: # Wenn Alle gezeigt wurden ...
            if now - self.cooldown >= self.blinkTime:
                if now - self.activationTick >= self.blinkTime:
                    self.disableAllChild()
                key = gameInput.check()
                self.checkInput(key)
                if len(self.query) == self.guessIndex: # Wenn fertig geratem
                    self.appendQuery()
                    self.blinkTime = self.blinkTime * 0.95
                    self.round += 1
                    self.index = 0
                    self.guessIndex = 0
                    self.activationTick = pygame.time.get_ticks()
                    pygame.mixer.Sound.play(self.roundFinishSound)
                    return
                if self.query[self.guessIndex] == self.guess:
                    self.guess = None
                    self.guessIndex += 1
                    self.score += 1
                    self.cooldown = pygame.time.get_ticks()
                elif self.guess:
                    self.guess = None
                    self.cooldown = pygame.time.get_ticks()
                    self.gameOver = True

                self.guess = None
            return
        
        if now - self.activationTick >= self.blinkTime: # Wenn das akt. Feld lang genug geleuchtet hat...
            # wechsle zum nächsten Feld
            current = self.query[self.index]
            self.disableAllChild()
            if current == "blue":
                self.topLeft.activate()
            elif current == "red":
                self.topRight.activate()
            elif current == "green":
                self.bottomLeft.activate()
            elif current == "yellow":
                self.bottomRight.activate()
            pygame.mixer.Sound.play(self.activeSound)
            self.index += 1
            self.activationTick = pygame.time.get_ticks()

    def disableAllChild(self):
        self.topLeft.deactivate()
        self.topRight.deactivate()
        self.bottomLeft.deactivate()
        self.bottomRight.deactivate()
            

    def checkInput(self, input):
        if input:
            if input == "up":
                self.guess = "blue"
                self.topLeft.activate()
                pygame.mixer.Sound.play(self.clickSound)
            elif input == "right":
                self.guess = "red"
                self.topRight.activate()
                pygame.mixer.Sound.play(self.clickSound)
            elif input == "left":
                self.guess = "green"
                self.bottomLeft.activate()
                pygame.mixer.Sound.play(self.clickSound)
            elif input == "down":
                self.guess = "yellow"
                self.bottomRight.activate()
                pygame.mixer.Sound.play(self.clickSound)

    def setRandomQuery(self):
        result = []
        for i in range(self.queryLength):
            pool = list(self.colorsToKey.keys())
            if i > 0:
                pool.remove(result[i - 1])
            choice = random.choice(pool)
            result.append(choice)
        self.query = result

    def appendQuery(self):
        pool = list(self.colorsToKey.keys())
        if self.queryLength > 0:
            pool.remove(self.query[self.queryLength - 1])
        choice = random.choice(pool)
        self.query.append(choice)
        self.queryLength += 1

    def reset(self):
        self.query = []
        self.queryLength = 0
        self.appendQuery()
        self.index = 0
        self.round = 0
        self.activationTick = pygame.time.get_ticks()
        self.guess = None
        self.guessIndex = 0
        self.cooldown = pygame.time.get_ticks()
        self.score = 0
        self.gameOver = False

            
class Corner:
    def __init__(self, screen, width, color, quadrant_n):
        self.screen = screen
        self.width = int(width)
        diagonal = width * math.sqrt(2)
        quadrant_2_centerX = screen.get_width() / 2
        quadrant_2_centerY = (screen.get_height() / 2) - (diagonal / 2)
        if quadrant_n == 3: 
            centerX = quadrant_2_centerX - (diagonal / 2)
            centerY = quadrant_2_centerY + (diagonal / 2)
        elif quadrant_n == 1:
            centerX = quadrant_2_centerX + (diagonal / 2)
            centerY = quadrant_2_centerY + (diagonal / 2)
        elif quadrant_n == 4:
            centerX = quadrant_2_centerX
            centerY = quadrant_2_centerY + diagonal
        elif quadrant_n == 2:
            centerX = quadrant_2_centerX
            centerY = quadrant_2_centerY
        (self.posX, self.posY) = getPosForCenterCord(centerX, centerY, width)
        self.active = False
        self.color = color
        self.blinkTime = 1000
        self.activationTick = pygame.time.get_ticks()
        # Images
        img = pygame.image.load(f'assets/{color}.png')
        img = pygame.transform.scale(img, (width, width))
        self.img, self.rect = rot_center(img, 45, centerX, centerY)
        img_disabled = pygame.image.load(f'assets/grey.png')
        img_disabled = pygame.transform.scale(img_disabled, (width, width))
        self.img_disabled, self.rect_disabled = rot_center(img_disabled, 45, centerX, centerY)

    def draw(self):
        if self.active:
            # ygame.draw.rect(self.screen, self.color, pygame.Rect(self.posX, self.posY, self.width, self.width))
            self.screen.blit(self.img, self.rect)
            # now = pygame.time.get_ticks()
            # if now - self.activationTick >= self.blinkTime:
            #     self.active = False
        else:
            self.screen.blit(self.img_disabled, self.rect_disabled)

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

class Text:
    def __init__(self, screen, text, size, color, offset):
        self.screen = screen
        self.font = pygame.font.Font('fonts/jersey.ttf', size)
        self.text = text
        self.size = size
        self.color = color
        self.offset = offset
        
    
    def draw(self):
        lines = self.text.splitlines()
        for i, l in enumerate(lines):
            text = self.font.render(l, True, self.color)
            posX = self.screen.get_width() / 2 - text.get_rect().width / 2
            posY = (self.screen.get_height() / 2 - text.get_rect().height / 2) + self.offset
            self.screen.blit(text, (posX, posY + self.size*i))
