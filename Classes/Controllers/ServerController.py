import time

import websocket
import rel
from threading import Thread
from queue import Queue
from DataClasses.ServerDataSerializer import ServerDataSerializer
from Classes.Enums.EventTypes import EventTypes
from Classes.Managers.LightManager import LightManager
from Classes.Managers.BoatManager import BoatManager
from DataClasses.BoatRoutes import BoatRoutes


class ServerController:
    def __init__(self):
        # the main looping thead which will be infinitely active
        self.boat_routes = BoatRoutes()
        self.main_thread = Thread(target=self.main_loop)
        self.boat_thread = Thread(target=self.boat_loop)
        rel.safe_read()
        self.queue = Queue()
        self.commands_queue = Queue()
        self.boat_queue = Queue()
        self.stop_threads = False
        websocket.enableTrace(True)

        self.ws = websocket.WebSocketApp(
            "ws://keyslam.com:8080",
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        # start a new thread which handles the websocket
        self.ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
        rel.signal(2, rel.abort)  # Keyboard Interrupt
        rel.dispatch()

    def boat_loop(self):
        boat_manager = BoatManager(self.ws)

        while True:
            route_id = self.boat_queue.get()
            second_route_id = -1
            if self.stop_threads:
                return

            boat_manager.setWarningLights("ON")
            boat_manager.requestBridgeRoadState()

            while True:
                request = self.commands_queue.get()

                if self.stop_threads:
                    return

                if request == "BRIDGE_EMPTY":
                    boat_manager.sethitTree("DOWN")
                elif request == "BARRIER_STATE_DOWN":
                    boat_manager.setBoatLight(route_id, "GREENRED")
                    boat_manager.setBridge("UP")
                elif request == "BRIDGE_STATE_UP":
                    boat_manager.setBoatLight(route_id, "GREEN")
                    boat_manager.requestBridgeWaterState()
                elif request == "WATER_EMPTY":
                    try:
                        other_id = self.boat_queue.get_nowait()
                        if second_route_id < 0:
                            second_route_id = other_id
                        if other_id == route_id:
                            boat_manager.setBoatLight(second_route_id, "RED")
                            time.sleep(8)
                            boat_manager.setBoatLight(route_id, "GREEN")
                        else:
                            boat_manager.setBoatLight(route_id, "RED")
                            time.sleep(8)
                            boat_manager.setBoatLight(second_route_id, "GREEN")
                        boat_manager.requestBridgeWaterState()
                    except:
                        if second_route_id > 0:
                            boat_manager.setBoatLight(second_route_id, "RED")

                        boat_manager.setBoatLight(route_id, "RED")
                        boat_manager.setBridge("DOWN")
                elif request == "BRIDGE_STATE_DOWN":
                    boat_manager.sethitTree("UP")
                elif request == "BARRIER_STATE_UP":
                    boat_manager.setWarningLights("OFF")
                    break
                else:
                    print(f"unknown request {request}")
                    break

    def main_loop(self):
        # create a new light manager which is only accessible in the main thread
        traffic_light_manager = LightManager(ws=self.ws)
        while True:
            # waits until we have some route_id in the queue
            route_id = self.queue.get()

            if self.stop_threads:
                return

            # turn traffic light route_id on
            threads = []
            traffic_light_manager.traffic_lights.set_route_state(route_id=route_id, state="GREEN")
            # create new thread for handling traffic light route_id
            thread = Thread(target=traffic_light_manager.activate_traffic_lights, args=[route_id, self.ws])
            # put reference thread in threads list
            threads.append(thread)
            thread.start()

            queue_length = self.queue.qsize()
            prev_routes = [route_id]
            i = 0

            while queue_length > i:
                route_id = self.queue.get()

                if self.stop_threads:
                    if len(threads) > 0:
                        for thread in threads:
                            thread.join()
                        return

                # if the route is already checked skip to next iteration
                if route_id in prev_routes:
                    i += 1
                    continue

                # if the route id's traffic light can be changed
                if traffic_light_manager.can_change_state(route_id=route_id):
                    traffic_light_manager.traffic_lights.set_route_state(route_id=route_id, state="GREEN")
                    # create new thread for handling traffic light route_id
                    thread = Thread(target=traffic_light_manager.activate_traffic_lights, args=[route_id, self.ws])
                    threads.append(thread)
                    thread.start()
                    prev_routes.append(route_id)
                else:
                    # else put route id's back into the queue
                    prev_routes.append(route_id)
                    self.queue.put(route_id)

                i += 1

            # end of while loop
            for thread in threads:
                thread.join()
                if self.stop_threads:
                    return

            # turn all traffic lights off
            traffic_light_manager.traffic_lights.reset()

    # starts a new thread when called
    def on_message(self, ws, message):
        dataSerializer = ServerDataSerializer()
        dataSerializer.load(message)
        self.check_on_message_event(dataSerializer)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("closed")

    def on_open(self, ws):
        print("Opened connection sending CONNECT_CONTROLLER")
        data = "{\"eventType\" : \"CONNECT_CONTROLLER\",  " \
               "\"data\" : " \
               "{ \"sessionName\" : \"session\", " \
               "\"sessionVersion\" : 1, " \
               "\"discardParseErrors\" : false,  " \
               "\"discardEventTypeErrors\" : false, " \
               "\"discardMalformedDataErrors\" : false, " \
               "\"discardInvalidStateErrors\" : false}" \
               "}"

        self.send_request(data)

    def check_on_message_event(self, dataSerializer):
        if dataSerializer.eventType == EventTypes.ERROR_NOT_PARSEABLE.name \
                or dataSerializer.eventType == EventTypes.ERROR_UNKNOWN_EVENT_TYPE.name \
                or dataSerializer.eventType == EventTypes.ERROR_MALFORMED_MESSAGE.name \
                or dataSerializer.eventType == EventTypes.ERROR_INVALID_STATE.name:
            print(dataSerializer.eventType)

        elif dataSerializer.eventType == EventTypes.ENTITY_ENTERED_ZONE.name:
            # adds the routeId to the queue which is accessible over the different threads
            if dataSerializer.data['routeId'] == self.boat_routes:
                self.boat_queue.put(dataSerializer.data['routeId'])
            else:
                self.queue.put(dataSerializer.data['routeId'])
        elif dataSerializer.eventType == EventTypes.ACKNOWLEDGE_BRIDGE_ROAD_EMPTY.name:
            self.commands_queue.put('BRIDGE_EMPTY')

        elif dataSerializer.eventType == EventTypes.ACKNOWLEDGE_BRIDGE_WATER_EMPTY.name:
            self.commands_queue.put('WATER_EMPTY')

        elif dataSerializer.eventType == EventTypes.ACKNOWLEDGE_BARRIERS_STATE.name:
            self.commands_queue.put(f"BARRIER_STATE_{dataSerializer.data['state']}")

        elif dataSerializer.eventType == EventTypes.ACKNOWLEDGE_BRIDGE_STATE.name:
            self.commands_queue.put(f"BRIDGE_STATE_{dataSerializer.data['state']}")

        elif dataSerializer.eventType == EventTypes.SESSION_START.name:
            print("started main thread")
            self.stop_threads = False
            self.main_thread = Thread(target=self.main_loop)
            self.boat_thread = Thread(target=self.boat_loop)
            self.main_thread.start()
            self.boat_thread.start()

        elif dataSerializer.eventType == EventTypes.SESSION_STOP.name:
            self.stop_threads = True
            self.queue.put(-1)
            self.boat_queue.put(-1)
            self.main_thread.join()
            self.boat_thread.join()
            with self.queue.mutex:
                self.queue.queue.clear()
            print("main thread killed")

    def send_request(self, data):
        print(f"we sent: {data}")
        self.ws.send(data)
