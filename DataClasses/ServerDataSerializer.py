from Classes.Enums.EventTypes import EventTypes
import json


class ServerDataSerializer:
    def __init__(self):
        self.eventType = None
        self.data = None

    def serialize(self) -> str:
        if self.data:
            return json.dumps({
                "eventType": self.eventType,
                "data": self.data
            })
        else:
            return json.dumps({
                "eventType": self.eventType
            })

    def load(self, json_data : str):
        dict = json.loads(json_data)
        self.eventType = EventTypes[dict['eventType']].name
        if "data" in dict.keys():
            self.data = dict['data']
        else:
            self.data = {}
