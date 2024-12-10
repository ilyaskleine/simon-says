from sensor import SensorController
from threading import Thread
from data import Data
from gamestate import GameState
from game_input import GameInput
import time

class Game:
    def __init__(self, sharedGameState):
        self.sharedGameState = sharedGameState

    def gameLoop(self):
        while True:
            print(self.sharedGameState.activeField)
            time.sleep(0.01)

sharedDataObject = Data()
sharedGameState = GameState()
sensorThread = Thread(target=SensorController().run, args=(sharedDataObject,))
sensorThread.start()
logicThread = Thread(target=GameInput(sharedDataObject, sharedGameState).run, args=())
logicThread.start()
game = Game(sharedGameState=sharedGameState)
game.gameLoop()


