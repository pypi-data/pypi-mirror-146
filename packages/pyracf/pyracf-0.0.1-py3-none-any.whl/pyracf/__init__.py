import importlib.resources
import json


class RACF:
    def parse(self, irrdbu00):
        with importlib.resources.open_text("pyracf", "offsets.json") as file:
            data = json.load(file)  
