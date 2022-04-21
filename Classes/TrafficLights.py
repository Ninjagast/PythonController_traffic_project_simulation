import csv
from Classes.Serializers.ServerDataSerializer import ServerDataSerializer
from Classes.Enums.EventTypes import EventTypes


class TrafficLights:
    def __init__(self, ws):
        self.lights = {}
        self.ws = ws

        with open('TrafficLights.csv', mode='r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                self.lights[int(row[0])] = row[1]

    def get_traffic_light(self, route_id: int) -> str:
        if route_id in self.lights.keys():
            return self.lights[route_id]
        raise NotImplementedError(f"{route_id} does not exist")

    def set_route_state(self, route_id : int, state: str):
        if route_id in self.lights.keys():
            self.lights[route_id] = state

    def reset(self):
        for route in self.lights:
            self.lights[route] = "red"
