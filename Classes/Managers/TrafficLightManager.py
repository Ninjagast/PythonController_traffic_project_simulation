from Classes.TrafficLights import TrafficLights


class TrafficLightManager:
    def __init__(self, ws):
        self.trafficLights = TrafficLights(ws)
        self.canPlayPattern = True

    def onEntityEntersZone(self, routeId, state):
        if self.canChangeState(routeId):
            self.canPlayPattern = False
            self.trafficLights.setRouteState(routeId, state)
        else:
            self.trafficLightPattern()

    def canChangeState(self, routeId):
        if routeId == 1 and (
                self.trafficLights.getTrafficLight(5) == 'red'
                and self.trafficLights.getTrafficLight(9) == 'red'):
            return True
        elif routeId == 2 and (
                self.trafficLights.getTrafficLight(5) == 'red'
                and self.trafficLights.getTrafficLight(9) == 'red'
                and self.trafficLights.getTrafficLight(10) == 'red'
                and self.trafficLights.getTrafficLight(11) == 'red'
                and self.trafficLights.getTrafficLight(12) == 'red'
        ):
            return True
        elif routeId == 3 and (
                self.trafficLights.getTrafficLight(5) == 'red'
                and self.trafficLights.getTrafficLight(7) == 'red'
                and self.trafficLights.getTrafficLight(8) == 'red'
                and self.trafficLights.getTrafficLight(11) == 'red'
                and self.trafficLights.getTrafficLight(12) == 'red'
                and self.trafficLights.getTrafficLight(15) == 'red'
        ):
            return True
        elif routeId == 4 and (
                self.trafficLights.getTrafficLight(8) == 'red'
                and self.trafficLights.getTrafficLight(12) == 'red'
                and self.trafficLights.getTrafficLight(15) == 'red'
        ):
            return True
        elif routeId == 5 and (
                self.trafficLights.getTrafficLight(1) == 'red'
                and self.trafficLights.getTrafficLight(2) == 'red'
                and self.trafficLights.getTrafficLight(3) == 'red'
                and self.trafficLights.getTrafficLight(8) == 'red'
                and self.trafficLights.getTrafficLight(9) == 'red'
                and self.trafficLights.getTrafficLight(11) == 'red'
                and self.trafficLights.getTrafficLight(12) == 'red'
                and self.trafficLights.getTrafficLight(15) == 'red'
        ):
            return True
        elif routeId == 7 and (
                self.trafficLights.getTrafficLight(3) == 'red'
                and self.trafficLights.getTrafficLight(11) == 'red'
                and self.trafficLights.getTrafficLight(15) == 'red'
        ):
            return True
        elif routeId == 8 and (
                self.trafficLights.getTrafficLight(3) == 'red'
                and self.trafficLights.getTrafficLight(4) == 'red'
                and self.trafficLights.getTrafficLight(5) == 'red'
                and self.trafficLights.getTrafficLight(11) == 'red'
                and self.trafficLights.getTrafficLight(12) == 'red'
        ):
            return True
        elif routeId == 9 and (
                self.trafficLights.getTrafficLight(1) == 'red'
                and self.trafficLights.getTrafficLight(2) == 'red'
                and self.trafficLights.getTrafficLight(5) == 'red'
                and self.trafficLights.getTrafficLight(11) == 'red'
                and self.trafficLights.getTrafficLight(12) == 'red'
        ):
            return True
        elif routeId == 10 and (self.trafficLights.getTrafficLight(2) == 'red'):
            return True
        elif routeId == 11 and (
                self.trafficLights.getTrafficLight(2) == 'red'
                and self.trafficLights.getTrafficLight(3) == 'red'
                and self.trafficLights.getTrafficLight(5) == 'red'
                and self.trafficLights.getTrafficLight(7) == 'red'
                and self.trafficLights.getTrafficLight(8) == 'red'
                and self.trafficLights.getTrafficLight(9) == 'red'
                and self.trafficLights.getTrafficLight(15) == 'red'
        ):
            return True
        elif routeId == 12 and (
                self.trafficLights.getTrafficLight(2) == 'red'
                and self.trafficLights.getTrafficLight(3) == 'red'
                and self.trafficLights.getTrafficLight(4) == 'red'
                and self.trafficLights.getTrafficLight(5) == 'red'
                and self.trafficLights.getTrafficLight(8) == 'red'
                and self.trafficLights.getTrafficLight(9) == 'red'
        ):
            return True
        elif routeId == 15 and (
                self.trafficLights.getTrafficLight(3) == 'red'
                and self.trafficLights.getTrafficLight(4) == 'red'
                and self.trafficLights.getTrafficLight(5) == 'red'
                and self.trafficLights.getTrafficLight(7) == 'red'
                and self.trafficLights.getTrafficLight(11) == 'red'
        ):
            return True
        else:
            return False

    def trafficLightPattern(self):
        if self.canPlayPattern:
            #         pattern 1:
            self.trafficLights.setRouteState(1, "green")
            self.trafficLights.setRouteState(2, "green")
            self.trafficLights.setRouteState(7, "green")
            self.trafficLights.setRouteState(8, "green")
            time.sleep(5)
            self.trafficLights.setRouteState(1, "orange")
            self.trafficLights.setRouteState(2, "orange")
            self.trafficLights.setRouteState(7, "orange")
            self.trafficLights.setRouteState(8, "orange")
            time.sleep(5)
            self.trafficLights.setRouteState(1, "red")
            self.trafficLights.setRouteState(2, "red")
            self.trafficLights.setRouteState(7, "red")
            self.trafficLights.setRouteState(8, "red")
            time.sleep(5)

            # pattern 2
            self.trafficLights.setRouteState(3, "green")
            self.trafficLights.setRouteState(4, "green")
            self.trafficLights.setRouteState(9, "green")
            self.trafficLights.setRouteState(10, "green")
            time.sleep(5)
            self.trafficLights.setRouteState(3, "orange")
            self.trafficLights.setRouteState(4, "orange")
            self.trafficLights.setRouteState(9, "orange")
            self.trafficLights.setRouteState(10, "orange")
            time.sleep(5)
            self.trafficLights.setRouteState(3, "red")
            self.trafficLights.setRouteState(4, "red")
            self.trafficLights.setRouteState(9, "red")
            self.trafficLights.setRouteState(10, "red")

            # pattern 3
            self.trafficLights.setRouteState(1, "green")
            self.trafficLights.setRouteState(7, "green")
            self.trafficLights.setRouteState(10, "green")
            self.trafficLights.setRouteState(12, "green")
            time.sleep(5)
            self.trafficLights.setRouteState(1, "orange")
            self.trafficLights.setRouteState(7, "orange")
            self.trafficLights.setRouteState(10, "orange")
            self.trafficLights.setRouteState(12, "orange")
            time.sleep(5)
            self.trafficLights.setRouteState(1, "red")
            self.trafficLights.setRouteState(7, "red")
            self.trafficLights.setRouteState(10, "red")
            self.trafficLights.setRouteState(12, "red")

            # pattern 4
            self.trafficLights.setRouteState(4, "green")
            self.trafficLights.setRouteState(5, "green")
            self.trafficLights.setRouteState(10, "green")
            self.trafficLights.setRouteState(11, "green")
            time.sleep(5)
            self.trafficLights.setRouteState(4, "orange")
            self.trafficLights.setRouteState(5, "orange")
            self.trafficLights.setRouteState(10, "orange")
            self.trafficLights.setRouteState(11, "orange")
            time.sleep(5)
            self.trafficLights.setRouteState(4, "red")
            self.trafficLights.setRouteState(5, "red")
            self.trafficLights.setRouteState(10, "red")
            self.trafficLights.setRouteState(11, "red")

            self.canPlayPattern = True
