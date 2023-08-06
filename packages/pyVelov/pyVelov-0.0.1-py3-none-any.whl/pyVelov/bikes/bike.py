class Bike:

    def __init__(self, data: dict):
        self.id = data["id"]
        self.number = data["number"]
        self.type = data["type"]
        self.status = data["status"]
        self.ratings = data["rating"]
        self.stationNumber = data["stationNumber"]
