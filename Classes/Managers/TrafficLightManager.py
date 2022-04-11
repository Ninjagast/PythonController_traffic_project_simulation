from Classes.TrafficLights import TrafficLights
import time
import threading


class TrafficLightManager:
    def __init__(self, ws):
        self.trafficLights = TrafficLights(ws)
        self.canPlayPattern = True

    def onEntityEntersZone(self, routeId):
        if self.canChangeState(routeId):
            thread = threading.Thread(target=self.activateTrafficLights, args=([routeId],))
            thread.start()
        else:
            self.trafficLightPattern()

    def givenTraficLightsAreRed(self, idArray):
        for id in idArray:
            if self.trafficLights.getTrafficLight(id) != 'red':
                return False
        return True

    def canChangeState(self, routeId):
        if routeId == 1 and self.givenTraficLightsAreRed([5, 9]):
            return True
        elif routeId == 2 and self.givenTraficLightsAreRed([5, 9, 10, 11, 12]):
            return True
        elif routeId == 3 and self.givenTraficLightsAreRed([5, 7, 8, 11, 12, 15]):
            return True
        elif routeId == 4 and self.givenTraficLightsAreRed([8, 12, 15]):
            return True
        elif routeId == 5 and self.givenTraficLightsAreRed([1, 2, 3, 8, 9, 11, 12, 15]):
            return True
        elif routeId == 7 and self.givenTraficLightsAreRed([3, 11, 15]):
            return True
        elif routeId == 8 and self.givenTraficLightsAreRed([3, 4, 5, 11, 12]):
            return True
        elif routeId == 9 and self.givenTraficLightsAreRed([1, 2, 5, 11, 12]):
            return True
        elif routeId == 10 and self.givenTraficLightsAreRed([2]):
            return True
        elif routeId == 11 and self.givenTraficLightsAreRed([2, 3, 5, 7, 8, 9, 15]):
            return True
        elif routeId == 12 and self.givenTraficLightsAreRed([2, 3, 4, 5, 8, 9]):
            return True
        elif routeId == 15 and self.givenTraficLightsAreRed([3, 4, 5, 7, 11]):
            return True
        else:
            return False

    def activateTrafficLights(self, idArray):
        self.canPlayPattern = False
        time.sleep(1)
        for id in idArray:
            self.trafficLights.setRouteState(id, 'GREEN')
        time.sleep(5)
        for id in idArray:
            self.trafficLights.setRouteState(id, 'ORANGE')
        time.sleep(5)
        for id in idArray:
            self.trafficLights.setRouteState(id, 'RED')
        self.canPlayPattern = True

    def trafficLightPattern(self):
        while not self.canPlayPattern:
            time.sleep(1)

        self.canPlayPattern = False
        # Pattern 1
        self.activateTrafficLights([1, 2, 7, 8])
        # Pattern 2
        self.activateTrafficLights([3, 4, 9, 10])
        # Pattern 3
        self.activateTrafficLights([1, 7, 10, 12])
        # Pattern 4
        self.activateTrafficLights([4, 5, 10, 11])

        self.canPlayPattern = True
