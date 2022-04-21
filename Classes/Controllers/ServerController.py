import websocket
import rel
import time
import json
from threading import Thread
from queue import Queue
from Classes.Serializers.ServerDataSerializer import ServerDataSerializer
from Classes.Enums.EventTypes import EventTypes
from Classes.Managers.TrafficLightManager import TrafficLightManager
from Classes.Managers.LightManager import LightManager


class ServerController:
    def __init__(self):
        # the main looping thead which will be infinitely active
        self.mainThread = Thread(target=self.main_loop)
        rel.safe_read()
        self.queue = Queue()
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

    # starts a new thread when called
    def on_message(self, ws, message):
        print(f"You got mail: {message}")

        dataSerializer = ServerDataSerializer()
        dataSerializer.load(message)
        self.check_on_message_event(dataSerializer)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    def on_open(self, ws):
        print("Opened connection sending CONNECT_CONTROLLER")
        data = "{\"eventType\" : \"CONNECT_CONTROLLER\",  " \
               "\"data\" : " \
               "{ \"sessionName\" : \"iets\", " \
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
        elif dataSerializer.eventType == EventTypes.ENTITY_EXITED_ZONE.name:
            pass
        elif dataSerializer.eventType == EventTypes.ENTITY_ENTERED_ZONE.name:
            # adds the routeId to the queue which is accessible over the different threads
            self.queue.put(dataSerializer.data['routeId'])
        elif dataSerializer.eventType == EventTypes.SESSION_START.name:
            print("started main thread")
            self.mainThread.start()
        elif dataSerializer.eventType == EventTypes.SESSION_STOP.name:
            pass

    def send_request(self, data):
        self.ws.send(data)

    def main_loop(self):
        traffic_light_manager = LightManager(self.ws)
        while True:
            # waits until we have some data in the queue
            data = self.queue.get()

            threads = []
            traffic_light_manager.trafficLights.setRouteState(data, "GREEN")
            threads.append(Thread(target=traffic_light_manager.activateTrafficLights, args=[data, self.ws]).start())
            queueLength = self.queue.qsize()
            prevRoutes = []
            prevRoutes.append(data)
            i = 0

            while queueLength > i:
                data = self.queue.get()
                if data in prevRoutes:
                    continue
                prevRoutes.append(data)
                if traffic_light_manager.canChangeState(data):
                    traffic_light_manager.trafficLights.setRouteState(data, "GREEN")
                    threads.append(
                        Thread(target=traffic_light_manager.activateTrafficLights, args=[data, self.ws]).start()
                    )
                else:
                    self.queue.put(data)

                i += 1

            for thread in threads:
                thread.join()
            traffic_light_manager.trafficLights.reset()

            print("GIVEN DATA:")
            print(data)
