import csv

class BoatRoutes:
    def __init__(self):
        self.boatRoutes = []
        self.initBoatRoutes()

    def __eq__(self, other):
        return other in self.boatRoutes


    def initBoatRoutes(self):
        with open('BoatLights.csv', mode='r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                self.boatRoutes.append(int(row[0]))


