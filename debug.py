from sensor import SensorController
from threading import Thread
from data import Data
from gamestate import GameState
from game_input import GameInput
import time

sharedDataObject = Data()
sharedGameState = GameState()
sensorThread = Thread(target=SensorController().run, args=(sharedDataObject,))
sensorThread.start()
logicThread = Thread(target=GameInput(sharedDataObject, sharedGameState).run, args=())
logicThread.start()

while True:
    print(f"F: {sharedDataObject.front}")
    print(f"B: {sharedDataObject.back}")
    print(f"R: {sharedDataObject.right}")
    print(f"L: {sharedDataObject.left}")
    print(f"Field: {sharedGameState.activeField}")
    time.sleep(1)



