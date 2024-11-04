import json

class Sensor:
    def __init__(self):
        pass
    
    def run(self, sharedDataObject):
        while True:
            with open('distances.json') as file:
                data = json.load(file)
            sharedDataObject.setValues(data["l"], data["r"], data["b"], data["f"])



    
