import pygame
import random

from graphic_objects import Text, Field

# Szene, die kontant im Hintergrund läuft (Sterne)
class BackgroundScene:
    def __init__(self, screen, backgroundOffset):
        # Parameter übernehmen
        self.screen = screen
        self.maxBackgroundOffset = backgroundOffset
        # Startwerte
        self.moving = False
        self.backgroundOffsetX = 0
        self.backgroundOffsetY = 0
        self.backgroundVelX = random.random()
        self.backgroundVelY = random.random()
        # Images
        self.backgroundImage = pygame.image.load(f'assets/background_dark.png')
        self.backgroundImage = pygame.transform.scale(self.backgroundImage, (screen.get_width() + self.maxBackgroundOffset * 2, screen.get_height() + self.maxBackgroundOffset * 2))
        self.lastMove = pygame.time.get_ticks()

    def draw(self):
        if pygame.time.get_ticks() - self.lastMove > 100 and self.moving:
            self.backgroundOffsetX += self.backgroundVelX
            self.backgroundOffsetY += self.backgroundVelY
            self.lastMove = pygame.time.get_ticks()
            if self.backgroundOffsetX >= self.maxBackgroundOffset or self.backgroundOffsetX <= -self.maxBackgroundOffset:
                self.backgroundVelX = self.backgroundVelX * -1
            if self.backgroundOffsetY >= self.maxBackgroundOffset or self.backgroundOffsetY <= -self.maxBackgroundOffset:
                self.backgroundVelY = self.backgroundVelY * -1
        self.screen.blit(self.backgroundImage, (-self.maxBackgroundOffset + self.backgroundOffsetX, -self.maxBackgroundOffset + self.backgroundOffsetY))

    def setMovement(self, isMoving):
        self.moving = isMoving

# Erste Szene des Spiels 
class StartScene:
    def __init__(self, screen):
        self.startTitle = Text(screen, "Simon Says", 100, (255, 255, 255), -100)
        self.startCaption = Text(screen, "Springe den gezeigten Farbcode\n und sammel Punkte!", 50, (255, 255, 255), 20)

    def draw(self):
        self.startTitle.draw()
        self.startCaption.draw()

class GameScene:
    def __init__(self, screen, gameInstance):
        self.screen = screen
        self.game = gameInstance
        self.mainBox = Field(screen, 400)

    def draw(self):
        self.game.background.setMovement(True)
        self.game.scene = self.mainBox.draw()

    def reset(self):
        self.mainBox.reset()

class GameOverScene:
    def __init__(self, screen, gameInstance):
        self.screen = screen
        self.game = gameInstance
        self.text = Text(self.screen, 'Game Over', 100, (255, 0, 0), 0)

    def draw(self):
        self.text.draw()