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

    def getTrafficLight(self, routeId):
        if routeId in self.lights.keys():
            return self.lights[routeId]
        raise NotImplementedError

    def setRouteState(self, routeId, state):
        if routeId in self.lights.keys():
            self.lights[routeId] = state

    def reset(self):
        for route in self.lights:
            self.lights[route] = "red"
