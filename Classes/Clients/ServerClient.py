import websocket
import _thread
import time
import rel
import json
from Classes.Serializers.DataSerializer import DataSerializer
from Classes.Enums.EventTypes import EventTypes
from Classes.Managers.TrafficLightManager import TrafficLightManager


class ServerClient:
    def __init__(self):
        rel.safe_read()
        websocket.enableTrace(True)

        self.ws = websocket.WebSocketApp(
            "ws://keyslam.com:8080",
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        self.traffic_light_manager = TrafficLightManager(self.ws)

        self.ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
        rel.signal(2, rel.abort)  # Keyboard Interrupt
        rel.dispatch()

    def on_message(self, ws, message):
        print(f"You got mail: {message}")

        dataSerializer = DataSerializer()
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
               "{ \"sessionName\" : \"burgerking\", " \
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
            self.traffic_light_manager.onEntityEntersZone(dataSerializer.data['routeId'])
        elif dataSerializer.eventType == EventTypes.SESSION_START.name:
            pass

    def send_request(self, data):
        self.ws.send(data)


