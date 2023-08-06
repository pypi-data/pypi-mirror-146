from .station import Station
from ..velov_api import Api
from typing import List

class Stations:

    def __init__(self):
        self.stations = []

    async def get_stations(self):
        stations = [Station(sation) for sation in await Api.get_stations()]
        return stations

    async def get_station(self, stationNumber: int) -> Station:

        station_data =  await Api.get_station(stationNumber)
        station = Station(station_data)
        return station

