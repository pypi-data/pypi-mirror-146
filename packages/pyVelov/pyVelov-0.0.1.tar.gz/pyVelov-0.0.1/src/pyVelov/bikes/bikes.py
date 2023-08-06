from ..velov_api import Api
from typing import List
from .bike import Bike

class Bikes:

    def __inti__(self):
        pass

    async def get_bikes(self) -> List[Bike]:
        bikes = await Api.get_bikes()
        return [Bike(bike_data) for bike_data in bikes]