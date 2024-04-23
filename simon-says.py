import pygame
import random

from game_input import GameInput
from graphic_objects import Field, Text

# --- Pygame Setup ---
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((720, 720));
pygame.display.set_caption("Farbfelder")
clock = pygame.time.Clock() 
running = True # Game Loop an aus 
dt = 0 # Für alles was sich bewegen würde
smallBoxWidth = 45;
smallBoxDistance = 250;

gameInput = GameInput(True)

scene = "startScreen"

# Erstellung der Grafikobjekte
mainBox = Field(screen, 400)
startTitle = Text(screen, "Simon Says", 100, (0, 0, 50), -100)
startCaption = Text(screen, "Springe den gezeigten Farbcode\n und sammel Punkte!", 50, (0, 0, 50), 20)
gameOverText = Text(screen, 'Game Over', 100, (255, 0, 0), 0)

sceneStart = pygame.time.get_ticks() 

# --- Game-Loop ---
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Hintergrund
    screen.fill("white")
    # Content

    if scene == "startScreen":
        screen.fill((240, 240, 255))
        startTitle.draw()
        startCaption.draw()
        if (pygame.time.get_ticks() - sceneStart) > 3000:
            scene = "game" 
    elif scene == "game":
        scene = mainBox.draw()
    elif scene == "gameOver":
        gameOverText.draw()

    pygame.display.flip()

    # Setzt FPS
    dt = clock.tick(30) / 1000 

pygame.quit()