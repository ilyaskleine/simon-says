from sensor import SensorController
from threading import Thread
from data import Data
from gamestate import GameState
from game_input import GameInput

sharedDataObject = Data()
sharedGameState = GameState()
sensorThread = Thread(target=SensorController().run, args=(sharedDataObject,))
sensorThread.start()
# logicThread = Thread(target=GameInput().run, args=(sharedDataObject, sharedGameState))
# logicThread.start()

while True:
    print(f"F: {sharedDataObject.front}")
    print(f"B: {sharedDataObject.back}")
    print(f"R: {sharedDataObject.right}")
    print(f"L {sharedDataObject.left}")
    print(f"Field: {sharedGameState.activeField}")



