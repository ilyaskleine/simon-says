import pygame
import random
from game_input import GameInput

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
gameInput = GameInput(False)

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
        self.topLeft = Corner(self.screen, self.posX, self.posY, cornerWidth, "blue")
        self.topRight = Corner(self.screen, self.posX + cornerWidth, self.posY, cornerWidth, "red")
        self.bottomLeft = Corner(self.screen, self.posX, self.posY  + cornerWidth, cornerWidth, "green")
        self.bottomRight = Corner(self.screen, self.posX + cornerWidth, self.posY + cornerWidth, cornerWidth, "yellow")
        # Algoritmic Variables
        self.reset()

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
        round_text = font.render(f'Runde {self.round + 1}', True, (0, 0, 0))
        self.screen.blit(round_text, (self.screen.get_width() - 130, 10))
        # return: Szenen die als nächstes folgen soll
        if self.gameOver:
            return "gameOver"
        else:
            return "game"

    def act(self):
        global scene
        now = pygame.time.get_ticks()
        if len(self.query) == self.index: # Wenn Alle gezeigt wurden ...
            #print("All were shown")
            if now - self.cooldown >= self.blinkTime:
                if now - self.activationTick >= self.blinkTime:
                    self.disableAllChild()
                key = gameInput.check()
                if not key == None:
                    print(key)
                self.checkInput(key)
                if len(self.query) == self.guessIndex: # Wenn fertig geratem
                    self.appendQuery()
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
                    self.gameOver = True
                    # => Implement Loosing Logic

                self.guess = None

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
            

    def checkInput(self, input):
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
    def __init__(self, screen, x, y, width, color):
        self.screen = screen
        self.width = int(width)
        self.posX = x
        self.posY = y
        self.active = False
        self.color = color
        self.blinkTime = 1000
        self.activationTick = pygame.time.get_ticks()
        img = pygame.image.load(f'assets/{color}.png')
        self.img = pygame.transform.scale(img, (width, width))

    def draw(self):
        if self.active:
            # ygame.draw.rect(self.screen, self.color, pygame.Rect(self.posX, self.posY, self.width, self.width))
            self.screen.blit(self.img, (self.posX, self.posY))
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

class Text:
    def __init__(self, screen, text, size, color, offset):
        self.screen = screen
        self.font = pygame.font.Font(None, size)
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
