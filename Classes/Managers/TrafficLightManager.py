from Classes.TrafficLights import TrafficLights
import time
import threading


class TrafficLightManager:
    def __init__(self, ws):
        self.trafficLights = TrafficLights(ws)
        self.canPlayPattern = True
        self.patternOrder = []
        self.bicycleRoutes = {21: "RED", 22: "RED", 23: "RED", 24: "RED"}
        self.pedestrianRoutes = {31: "RED", 32: "RED", 33: "RED", 34: "RED", 35: "RED", 36: "RED", 37: "RED", 38: "RED"}
        self.threads = []


    def onEntityEntersZone(self, routeId):
        if self.canChangeState(routeId):
            self.canPlayPattern = False
            thread = threading.Thread(target=self.activateTrafficLights, args=([routeId],))
            self.threads.append(thread)
            thread.start()
            print(routeId)
        else:
            if len(self.threads) > 0:
                for thread in self.threads:
                    thread.join()
                self.threads = []
                self.canPlayPattern = True

            if routeId in self.bicycleRoutes.keys():
                self.bicycleRoutes[routeId] = "GREEN"

            if routeId in self.pedestrianRoutes.keys():
                self.pedestrianRoutes[routeId] = "GREEN"

            if self.getPattern(routeId) not in self.patternOrder:
                self.addPatternToPatternOrder(self.getPattern(routeId))

            if self.canPlayPattern:
                self.canPlayPattern = False
                self.playPattern()
            else:
                print('log daar is wat')
                return

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
        elif routeId == 5 and self.givenTraficLightsAreRed([1, 2, 3, 8, 9, 10, 11, 12, 15]):
            return True
        elif routeId == 7 and self.givenTraficLightsAreRed([3, 11, 15]):
            return True
        elif routeId == 8 and self.givenTraficLightsAreRed([3, 4, 5, 11, 12]):
            return True
        elif routeId == 9 and self.givenTraficLightsAreRed([1, 2, 5, 11, 12]):
            return True
        elif routeId == 10 and self.givenTraficLightsAreRed([2, 5]):
            return True
        elif routeId == 11 and self.givenTraficLightsAreRed([2, 3, 5, 7, 8, 9, 15]):
            return True
        elif routeId == 12 and self.givenTraficLightsAreRed([2, 3, 4, 5, 8, 9]):
            return True
        elif routeId == 15 and self.givenTraficLightsAreRed([3, 4, 5, 7, 11]):
            return True
        elif routeId == 21 and self.givenTraficLightsAreRed([1, 2, 3, 4, 8, 12]):
            return True
        elif routeId == 22 and self.givenTraficLightsAreRed([3, 4, 5, 7, 11]):
            return True
        elif routeId == 23 and self.givenTraficLightsAreRed([2, 5, 7, 8, 9, 10, ]):
            return True
        elif routeId == 24 and self.givenTraficLightsAreRed([1, 5, 9, 10, 11, 12]):
            return True
        elif (routeId == 31 or routeId == 32) and self.givenTraficLightsAreRed([1, 2, 3, 4, 8, 12]):
            return True
        elif (routeId == 33 or routeId == 34) and self.givenTraficLightsAreRed([3, 4, 5, 7, 11]):
            return True
        elif (routeId == 35 or routeId == 36) and self.givenTraficLightsAreRed([2, 5, 7, 8, 9, 10, ]):
            return True
        elif (routeId == 37 or routeId == 38) and self.givenTraficLightsAreRed([1, 5, 9, 10, 11, 12]):
            return True
        else:
            return False

    def activateTrafficLights(self, idArray, deactivateEarlyIds=None, activateLaterIds=None):
        # time.sleep(1)
        sleepTime = 5
        # turn traffic lights in idArray to green
        for id in idArray:
            self.trafficLights.setRouteState(id, 'GREEN')
        # turn traffic lights in deactivateEarlyIds from green to orange to red
        if deactivateEarlyIds is not None:
            time.sleep(3)
            self.deactivateTrafficLights(deactivateEarlyIds)
        # turn traffic lights in activateLaterIds to green
        if activateLaterIds is not None:
            for id in activateLaterIds:
                self.trafficLights.setRouteState(id, 'GREEN')
                if id in [21, 22, 23, 24]:
                    sleepTime = 7
                elif id in [31, 32, 33, 34, 35, 36, 37, 38]:
                    sleepTime = 10

        time.sleep(sleepTime)
        # turn traffic lights in activateLaterIds from green to orange to red
        if activateLaterIds is not None:
            self.deactivateTrafficLights(activateLaterIds)
        # turn traffic lights in idArray from green to orange to red
        self.deactivateTrafficLights(idArray)

    def deactivateTrafficLights(self, idArray):
        for id in idArray:
            if self.isPedestrianRoute(id):
                self.trafficLights.setRouteState(id, 'BLINKING')
            else:
                self.trafficLights.setRouteState(id, 'ORANGE')
        time.sleep(5)
        for id in idArray:
            self.trafficLights.setRouteState(id, 'RED')

    def isPedestrianRoute(self, routeId):
        return routeId in [31, 32, 33, 34, 35, 36, 37, 38]

    def addPatternToPatternOrder(self, pattern):
        self.patternOrder.append(pattern)

    def playPattern(self):
        while len(self.patternOrder) > 0:
            self.executePattern(self.patternOrder[0])
        self.canPlayPattern = True

    def getPattern(self, routeId):
        if routeId in [1, 2, 8, 22, 24]:
            return "pattern1"
        elif routeId in [3, 9]:
            return "pattern2"
        elif routeId in [7, 10, 12]:
            return "pattern3"
        elif routeId in [11, 21, 23]:
            return "pattern4"
        elif routeId in [4, 5]:
            return "pattern5"

    def executePattern(self, pattern):
        print(self.patternOrder)
        # todo: voetgangers toevoegen aan patreunn
        self.canPlayPattern = False
        if pattern == "pattern1":
            # Pattern 1
            if self.bicycleRoutes[22] == 'GREEN' or self.bicycleRoutes[24] == 'GREEN':
                self.activateTrafficLights([1, 2, 7, 8], [7, 8], [22, 24])
                self.bicycleRoutes[22] = 'RED'
                self.bicycleRoutes[24] = 'RED'
            else:
                self.activateTrafficLights([1, 2, 7, 8])
        elif pattern == "pattern2":
            # Pattern 2
            self.activateTrafficLights([3, 4, 9, 10])
        elif pattern == "pattern3":
            # Pattern 3
            self.activateTrafficLights([1, 7, 10, 12])
        elif pattern == "pattern4":
            # Pattern 4
            if self.bicycleRoutes[21] == 'GREEN' or self.bicycleRoutes[23] == 'GREEN':
                self.activateTrafficLights([4, 10, 11], [4, 10], [21, 23])
                self.bicycleRoutes[21] = 'RED'
                self.bicycleRoutes[23] = 'RED'
            else:
                self.activateTrafficLights([4, 10, 11])
        elif pattern == "pattern5":
            # Pattern 5
            self.activateTrafficLights([4, 5, 7])

        if len(self.patternOrder) > 0:
            self.patternOrder.pop(0)
