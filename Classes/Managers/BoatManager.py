from DataClasses.ServerDataSerializer import ServerDataSerializer


class BoatManager:

    def __init__(self, ws):
        self.hitTreeIsUp = False
        self.warningLightIsOn = False
        self.bridgeIsUp = False
        self.boatLightIsOn = False

    def setBridge(self, state):
        data = ServerDataSerializer()
        data.eventType = EventTypes.REQUEST_BRIDGE_STATE.name
        data.data = {
            'state': state
        }
        ws.send(data.serialize())

    def sethitTree(self, state):
        data = ServerDataSerializer()
        data.eventType = EventTypes.REQUEST_BARRIERS_STATE.name
        data.data = {
            'state': state
        }
        ws.send(data.serialize())

    def setBoatLight(self, route_id: int, state: string):
        data = ServerDataSerializer()
        data.eventType = EventTypes.SET_BOAT_ROUTE_STATE.name
        data.data = {
            'id': route_id,
            'state': state
        }
        ws.send(data.serialize())

    def setWarningLights(self, state):
        data = ServerDataSerializer()
        data.eventType = EventTypes.SET_BRIDGE_WARNING_LIGHT_STATE.name
        data.data = {
            'state': state
        }
        ws.send(data.serialize())

    def requestBridgeRoadState(self):
        data = ServerDataSerializer()
        data.eventType = EventTypes.REQUEST_BRIDGE_ROAD_EMPTY.name
        ws.send(data.serialize())

    def requestBridgeWaterState(self):
        data = ServerDataSerializer()
        data.eventType = EventTypes.REQUEST_BRIDGE_WATER_EMPTY.name
        ws.send(data.serialize())
