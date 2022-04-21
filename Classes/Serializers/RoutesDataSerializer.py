import json


class RoutesDataSerializer:
    def __init__(self):
        self.data = None
        with open('routesList.json', mode='r') as json_file:
            self.data = json.loads(json_file.read())

    def get_route_data(self) -> dict:
        return self.data
