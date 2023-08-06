from .station import Station
from ..velov_api import Api
from typing import List

class Stations:

    def __init__(self):
        self.stations = []

    def get_stations(self):
        stations = [Station(sation) for sation in Api.get_stations()]
        return stations

    def get_station(self, stationNumber: int) -> Station:

        station_data = Api.get_station(stationNumber)
        station = Station(station_data)
        return station

