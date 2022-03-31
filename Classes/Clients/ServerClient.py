import websocket
import _thread
import time
import rel
import json
from Classes.Serializers.DataSerializer import DataSerializer
from Classes.Enums.EventTypes import EventTypes


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
               "{ \"sessionName\" : \"KFC\", " \
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
        elif dataSerializer.eventType == EventTypes.ACKNOWLEDGE_BRIDGE_STATE.name:
            print('henkie')
        elif dataSerializer.eventType == EventTypes.SESSION_START.name:
            self.allGreen()
            # pass

    def send_request(self, data):
        self.ws.send(data)

    def allGreen(self):
        time.sleep(10)
        data = DataSerializer()
        data.eventType = EventTypes.SET_AUTOMOBILE_ROUTE_STATE.name
        # CARS:
        data.data = {
            "routeId": 1,
            "state": "GREEN"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 2,
            "state": "GREEN"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 3,
            "state": "GREEN"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 10,
            "state": "GREEN"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 11,
            "state": "GREEN"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 12,
            "state": "GREEN"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 7,
            "state": "GREEN"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 8,
            "state": "GREEN"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 9,
            "state": "GREEN"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 5,
            "state": "GREEN"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 4,
            "state": "GREEN"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 15,
            "state": "GREEN"
        }
        self.send_request(data.serialize())

        #     END CARS

        # START CYCLIST
        data.eventType = EventTypes.SET_CYCLIST_ROUTE_STATE.name

        data.data = {
            "routeId": 24,
            "state": "GREEN"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 23,
            "state": "GREEN"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 22,
            "state": "GREEN"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 21,
            "state": "GREEN"
        }
        self.send_request(data.serialize())
        # END CYCLIST
        # START PEDESTRIAN
        data.eventType = EventTypes.SET_PEDESTRIAN_ROUTE_STATE.name
        data.data = {
            "routeId": 31,
            "state": "GREEN"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 32,
            "state": "GREEN"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 33,
            "state": "GREEN"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 34,
            "state": "GREEN"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 35,
            "state": "GREEN"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 36,
            "state": "GREEN"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 37,
            "state": "GREEN"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 38,
            "state": "GREEN"
        }
        self.send_request(data.serialize())
        # END PEDESTRIAN

        self.allOrange()

    def allOrange(self):
        time.sleep(10)
        data = DataSerializer()
        data.eventType = EventTypes.SET_AUTOMOBILE_ROUTE_STATE.name
        # CARS:
        data.data = {
            "routeId": 1,
            "state": "ORANGE"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 2,
            "state": "ORANGE"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 3,
            "state": "ORANGE"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 10,
            "state": "ORANGE"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 11,
            "state": "ORANGE"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 12,
            "state": "ORANGE"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 7,
            "state": "ORANGE"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 8,
            "state": "ORANGE"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 9,
            "state": "ORANGE"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 5,
            "state": "ORANGE"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 4,
            "state": "ORANGE"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 15,
            "state": "ORANGE"
        }
        self.send_request(data.serialize())

        #     END CARS

        # START CYCLIST
        data.eventType = EventTypes.SET_CYCLIST_ROUTE_STATE.name

        data.data = {
            "routeId": 24,
            "state": "ORANGE"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 23,
            "state": "ORANGE"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 22,
            "state": "ORANGE"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 21,
            "state": "ORANGE"
        }
        self.send_request(data.serialize())
        # END CYCLIST
        # START PEDESTRIAN
        data.eventType = EventTypes.SET_PEDESTRIAN_ROUTE_STATE.name
        data.data = {
            "routeId": 31,
            "state": "BLINKING"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 32,
            "state": "BLINKING"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 33,
            "state": "BLINKING"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 34,
            "state": "BLINKING"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 35,
            "state": "BLINKING"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 36,
            "state": "BLINKING"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 37,
            "state": "BLINKING"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 38,
            "state": "BLINKING"
        }
        self.send_request(data.serialize())
        # END PEDESTRIAN

        self.lastTest()


    def lastTest(self):
        time.sleep(10)
        data = DataSerializer()
        data.eventType = EventTypes.SET_AUTOMOBILE_ROUTE_STATE.name
        # CARS:
        data.data = {
            "routeId": 1,
            "state": "GREEN"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 2,
            "state": "GREEN"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 3,
            "state": "RED"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 10,
            "state": "RED"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 11,
            "state": "RED"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 12,
            "state": "RED"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 7,
            "state": "RED"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 8,
            "state": "GREEN"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 9,
            "state": "RED"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 5,
            "state": "RED"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 4,
            "state": "RED"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 15,
            "state": "RED"
        }
        self.send_request(data.serialize())

        #     END CARS

        # START CYCLIST
        data.eventType = EventTypes.SET_CYCLIST_ROUTE_STATE.name

        data.data = {
            "routeId": 24,
            "state": "RED"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 23,
            "state": "RED"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 22,
            "state": "GREEN"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 21,
            "state": "RED"
        }
        self.send_request(data.serialize())
        # END CYCLIST
        # START PEDESTRIAN
        data.eventType = EventTypes.SET_PEDESTRIAN_ROUTE_STATE.name
        data.data = {
            "routeId": 31,
            "state": "RED"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 32,
            "state": "RED"
        }
        self.send_request(data.serialize())

        data.data = {
            "routeId": 33,
            "state": "GREEN"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 34,
            "state": "GREEN"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 35,
            "state": "RED"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 36,
            "state": "RED"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 37,
            "state": "RED"
        }
        self.send_request(data.serialize())
        data.data = {
            "routeId": 38,
            "state": "RED"
        }
        self.send_request(data.serialize())
        # END PEDESTRIAN

