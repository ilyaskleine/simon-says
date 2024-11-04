import pygame

from threading import Thread
from scenes import StartScene, BackgroundScene, GameScene, GameOverScene
from data import Data
from sensor_debug import Sensor

class Game:
    def __init__(self, debug, sharedDataObject):
        self.debug = debug
        # --- Pygame Setup ---
        pygame.init()
        pygame.font.init()
        if self.debug:
            self.screen = pygame.display.set_mode((1000, 720))
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Farbfelder")
        self.clock = pygame.time.Clock() 
        self.running = True # Game Loop an aus 
        self.dt = 0 # Für alles was sich bewegen würde
        self.smallBoxWidth = 45;
        self.smallBoxDistance = 250;

        self.scene = "game" if debug else "startscreen"

        # Szenen 
        self.background = BackgroundScene(self.screen, 20)
        self.startScene = StartScene(self.screen)
        self.gameOverScene = GameOverScene(self.screen, self)
        self.gameScene = GameScene(self.screen, self, sharedDataObject)

        self.sceneStart = pygame.time.get_ticks() 

    def gameLoop(self, sharedDataObject):
        # --- Game-Loop ---
        while self.running:
            # Beenden des Programms
            keys = pygame.key.get_pressed()
            if keys[pygame.K_x]:
                self.running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Hintergrund
            self.background.draw()

            # Content
            if self.scene == "startscreen":
                self.startScene.draw()
                if (pygame.time.get_ticks() - self.sceneStart) > 3000:
                    self.scene = "game"
                    self.sceneStart = pygame.time.get_ticks()
            elif self.scene == "game":
                self.gameScene.draw()
                self.sceneStart = pygame.time.get_ticks()
            elif self.scene == "gameOver":
                self.background.setMovement(False)
                self.gameOverScene.draw()
                if (pygame.time.get_ticks() - self.sceneStart) > 3000:
                    self.scene = "game" if self.debug else "startscreen"
                    self.sceneStart = pygame.time.get_ticks()
                    self.gameScene.reset()

            if self.debug:
                font = pygame.font.Font(None, 25)
                debug_text = font.render(f'[Debug Mode]', True, (255, 0, 0))
                self.screen.blit(debug_text, (10, self.screen.get_height() - 120))
                round_text = font.render(f'X schließt Programm', True, (255, 0, 0))
                self.screen.blit(round_text, (10, self.screen.get_height() - 100))
                #data = self.keyboard_input.debug()
                #if data is None:
                #    print("No Sensor-Data")
                #else:
                #    l_text = font.render(f'l_value: {data["l"]}', True, (0, 0, 0))
                #    self.screen.blit(l_text, (10, self.screen.get_height() - 80))
                #    r_text = font.render(f'r_value: {data["r"]}', True, (0, 0, 0))
                #    self.screen.blit(r_text, (10, self.screen.get_height() - 60))
                #    f_text = font.render(f'f_value: {data["f"]}', True, (0, 0, 0))
                #    self.screen.blit(f_text, (10, self.screen.get_height() - 40))
                #    b_text = font.render(f'b_value: {data["b"]}', True, (0, 0, 0))
                #    self.screen.blit(b_text, (10, self.screen.get_height() - 20))
            
            pygame.display.flip()

            # Setzt FPS
            self.dt = self.clock.tick(30) / 1000

        pygame.quit()

sharedDataObject = Data()

game = Game(debug=True, sharedDataObject=sharedDataObject)
gameThread = Thread(target=game.gameLoop, args=(sharedDataObject,))
gameThread.start()
sensorThread = Thread(target=Sensor().run, args=(sharedDataObject,))
sensorThread.start()

