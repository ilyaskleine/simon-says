from sensor_debug import Sensor
from data_classes import SensorData, LogicData
from gamestate import GameState
from game_input import GameInput
import time
from threading import Thread

class Game:
    def __init__(self, sharedGameState):
        self.sharedGameState = sharedGameState

    def gameLoop(self):
        while True:
            print(self.sharedGameState.activeField)
            time.sleep(0.01)

sharedDataObject = SensorData()
sharedGameState = LogicData()
sensorThread = Thread(target=Sensor().run, args=(sharedDataObject,))
sensorThread.start()
logicThread = Thread(target=GameInput(sharedDataObject, sharedGameState).run, args=())
logicThread.start()
game = Game(sharedGameState=sharedGameState)
game.gameLoop()


