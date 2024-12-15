from thread_sensor import SensorThread
from data_classes import SensorData, LogicData
from thread_logic import LogicThread
import time
from threading import Thread

class Game:
    def __init__(self, sharedGameState):
        self.sharedGameState = sharedGameState

    def gameLoop(self):
        while True:
            #print(self.sharedGameState.left)
            #print(self.sharedGameState.right)
            #print(self.sharedGameState.front)
            print(self.sharedGameState.back)
            time.sleep(0.01)

sharedDataObject = SensorData()
sharedGameState = LogicData()
sensorThread = Thread(target=SensorThread().run, args=(sharedDataObject,))
sensorThread.start()
logicThread = Thread(target=LogicThread(sharedDataObject, sharedGameState).run, args=())
logicThread.start()
game = Game(sharedGameState=sharedDataObject)
game.gameLoop()


