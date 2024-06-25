import json

class SensorData:
    def __init__(self):
        pass
    
    def getAll(self):
        with open('distances.json') as file:
            data = json.load(file)
        return {"l": data["l"], "r": data["r"], "b": data["b"], "f": data["f"]}



    
