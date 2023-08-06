from .stations.stations import Stations
from .bikes.bikes import Bikes

from .velov_api import Api

class Velov:

    def __init__(self):
        self.stations: Stations = Stations()
        self.bikes: Bikes = Bikes()

    async def start(self):
        await Api.set_tokens()
