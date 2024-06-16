import pygame
import random

from graphic_objects import Field, Text
from game_input import GameInput

debug = True

# --- Pygame Setup ---
pygame.init()
pygame.font.init()
if debug:
    screen = pygame.display.set_mode((1000, 720))
else:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Farbfelder")
clock = pygame.time.Clock() 
running = True # Game Loop an aus 
dt = 0 # Für alles was sich bewegen würde
smallBoxWidth = 45;
smallBoxDistance = 250;

scene = "game" if debug else "startScreen"

keyboard_input = GameInput(True)

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
    screen.fill((255, 255, 255))

    # Content
    if scene == "startScreen":
        screen.fill((240, 240, 255))
        startTitle.draw()
        startCaption.draw()
        if (pygame.time.get_ticks() - sceneStart) > 3000:
            scene = "game"
            sceneStart = pygame.time.get_ticks()
    elif scene == "game":
        scene = mainBox.draw()
        sceneStart = pygame.time.get_ticks()
    elif scene == "gameOver":
        gameOverText.draw()
        if (pygame.time.get_ticks() - sceneStart) > 3000:
            scene = "game" if debug else "startScreen"
            sceneStart = pygame.time.get_ticks()
            mainBox.reset()

    if debug:
        keys = keyboard_input.get_pressed()
        if keys[pygame.K_x]:
            running = False
        font = pygame.font.Font(None, 25)
        debug_text = font.render(f'[Debug Mode]', True, (255, 0, 0))
        screen.blit(debug_text, (10, screen.get_height() - 120))
        round_text = font.render(f'X schließt Programm', True, (255, 0, 0))
        screen.blit(round_text, (10, screen.get_height() - 100))
        data = keyboard_input.debug()
        l_text = font.render(f'l_value: {data["l"]}', True, (0, 0, 0))
        screen.blit(l_text, (10, screen.get_height() - 80))
        r_text = font.render(f'r_value: {data["r"]}', True, (0, 0, 0))
        screen.blit(r_text, (10, screen.get_height() - 60))
        f_text = font.render(f'f_value: {data["f"]}', True, (0, 0, 0))
        screen.blit(f_text, (10, screen.get_height() - 40))
        b_text = font.render(f'b_value: {data["b"]}', True, (0, 0, 0))
        screen.blit(b_text, (10, screen.get_height() - 20))
    
    pygame.display.flip()

    # Setzt FPS
    dt = clock.tick(30) / 1000

pygame.quit()