import json

class Sensor:
    def __init__(self):
        pass
    
    def run(self, sharedDataObject):
        while True:
            with open('distances.json') as file:
                data = json.load(file)
            sharedDataObject.left = data["l"]
            sharedDataObject.right = data["r"]
            sharedDataObject.front = data["f"]
            sharedDataObject.back = data["b"]



    
