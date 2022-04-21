from Classes.TrafficLights import TrafficLights
import time
import threading
from Classes.Serializers.RoutesDataSerializer import RoutesDataSerializer
from Classes.Serializers.ServerDataSerializer import ServerDataSerializer
from Classes.Enums.EventTypes import EventTypes

class LightManager:

    def __init__(self, ws):
        self.trafficLights = TrafficLights(ws)
        self.routeData = RoutesDataSerializer().getRouteData()

    def canChangeState(self, routeId: int) -> bool:
        for id in self.routeData.get(str(routeId)):
            if self.trafficLights.getTrafficLight(id) != 'red':
                return False
        return True

    def getServerRequestJSON(self, routeId: int, state: str) -> str:
        data = ServerDataSerializer()
        if routeId in [21, 22, 23, 24]:
            data.eventType = EventTypes.SET_CYCLIST_ROUTE_STATE.name
        elif routeId in [31, 32, 33, 34, 35, 36, 37, 38]:
            data.eventType = EventTypes.SET_PEDESTRIAN_ROUTE_STATE.name
        else:
            data.eventType = EventTypes.SET_AUTOMOBILE_ROUTE_STATE.name
        data.data = {
            "routeId": routeId,
            "state": state
        }
        return data.serialize()

    def activateTrafficLights(self, routeId: int, ws):
        sleepTime = 5
        if self.isBicycleRoute(routeId):
            sleepTime = 7
        elif self.isPedestrianRoute(routeId):
            sleepTime = 10

        request = self.getServerRequestJSON(routeId, "GREEN")
        ws.send(request)

        time.sleep(sleepTime)
        # turn traffic lights in idArray from green to orange to red
        self.deactivateTrafficLights(routeId, sleepTime, ws)

    def deactivateTrafficLights(self, routeId: int, sleepTime: int, ws):
        if self.isPedestrianRoute(routeId):
            request = self.getServerRequestJSON(routeId, "BLINKING")
        else:
            request = self.getServerRequestJSON(routeId, "ORANGE")

        ws.send(request)

        time.sleep(sleepTime)

        request = self.getServerRequestJSON(routeId, "RED")
        ws.send(request)

    def isPedestrianRoute(self, routeId):
        return routeId in [31, 32, 33, 34, 35, 36, 37, 38]

    def isBicycleRoute(self, routeId):
        return routeId in [21, 22, 23, 24]
