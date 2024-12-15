import json
import time

class SensorThread:
    def __init__(self):
        pass
    
    def run(self, sharedDataObject):
        while True:
            with open('distances.json') as file:
                data = json.load(file)
            sharedDataObject.left = data["l"]
            time.sleep(0.01)
            sharedDataObject.right = data["r"]
            time.sleep(0.01)
            sharedDataObject.front = data["f"]
            time.sleep(0.01)
            sharedDataObject.back = data["b"]
            time.sleep(0.01)



    
