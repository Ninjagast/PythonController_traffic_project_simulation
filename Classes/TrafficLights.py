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

            data = ServerDataSerializer()
            if routeId in [21, 22, 23, 24]:
                data.eventType = EventTypes.SET_CYCLIST_ROUTE_STATE.name
            elif routeId in [31, 32, 33, 34, 35, 36, 37, 38]:
                data.eventType = EventTypes.SET_PEDESTRIAN_ROUTE_STATE.name
            else:
                data.eventType = EventTypes.SET_AUTOMOBILE_ROUTE_STATE.name
            data.data = {
                "routeId": int(routeId),
                "state": state
            }
            self.ws.send(data.serialize())

