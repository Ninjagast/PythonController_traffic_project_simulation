from Classes.TrafficLights import TrafficLights
import time
import threading
from Classes.Serializers.RoutesDataSerializer import RoutesDataSerializer
from Classes.Serializers.ServerDataSerializer import ServerDataSerializer
from Classes.Enums.EventTypes import EventTypes


class LightManager:

    def __init__(self, ws):
        self.traffic_lights = TrafficLights(ws=ws)
        self.route_data = RoutesDataSerializer().get_route_data()

    def can_change_state(self, route_id: int) -> bool:
        for id in self.route_data.get(str(route_id)):
            if self.traffic_lights.get_traffic_light(route_id=id) != 'red':
                return False
        return True

    def get_server_request_JSON(self, route_id: int, state: str) -> str:
        data = ServerDataSerializer()
        if route_id in [21, 22, 23, 24]:
            data.eventType = EventTypes.SET_CYCLIST_ROUTE_STATE.name
        elif route_id in [31, 32, 33, 34, 35, 36, 37, 38]:
            data.eventType = EventTypes.SET_PEDESTRIAN_ROUTE_STATE.name
        else:
            data.eventType = EventTypes.SET_AUTOMOBILE_ROUTE_STATE.name
        data.data = {
            "routeId": route_id,
            "state": state
        }
        return data.serialize()

    def activate_traffic_lights(self, route_id: int, ws):
        sleep_time = 5
        if self.is_bicycle_route(route_id=route_id):
            sleep_time = 7
        elif self.is_pedestrian_route(route_id=route_id):
            sleep_time = 10

        request = self.get_server_request_JSON(route_id=route_id, state="GREEN")
        ws.send(request)

        time.sleep(sleep_time)
        # turn traffic lights in idArray from green to orange to red
        self.deactivate_traffic_lights(route_id=route_id, sleep_time=sleep_time, ws=ws)

    def deactivate_traffic_lights(self, route_id: int, sleep_time: int, ws):
        if self.is_pedestrian_route(route_id=route_id):
            request = self.get_server_request_JSON(route_id=route_id, state="BLINKING")
        else:
            request = self.get_server_request_JSON(route_id=route_id, state="ORANGE")

        ws.send(request)
        time.sleep(sleep_time)
        request = self.get_server_request_JSON(route_id=route_id, state="RED")
        ws.send(request)

    def is_pedestrian_route(self, route_id: int) -> bool:
        return route_id in [31, 32, 33, 34, 35, 36, 37, 38]

    def is_bicycle_route(self, route_id: int) -> bool:
        return route_id in [21, 22, 23, 24]
