import aiohttp
import asyncio

class VelovApi:


    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.refreshToken = None
        self.accessToken = None

        self.BASE_URL = "https://api.cyclocity.fr/"
        self.START_AUTH_URL = self.BASE_URL + "auth/environments/PRD/client_tokens"
        self.AUTH_DATA = {
            "code": "vls.web.lyon:PRD",
            "key": "c3d9f5c22a9157a7cc7fe0e38269573bdd2f13ec48f867360ecdcbd35b196f87"
        }

    async def set_tokens(self):
        response = await self.session.post(self.START_AUTH_URL, json=self.AUTH_DATA)
        response = await response.json()
        self.refreshToken = response['refreshToken']
        self.accessToken = response["accessToken"]
        self.session.headers.add("Authorization", f"Taknv1 {self.accessToken}")

        print("Done getting tokens")

    async def get_station(self, stationNumber: int):
        url = f"{self.BASE_URL}contracts/lyon/stations/{stationNumber}"
        response = await self.session.get(
            url,
            headers={"Content-Type": "application/vnd.station.v4+json"}
        )
        return await response.json()

    async def get_stations(self):
        url = f"{self.BASE_URL}contracts/lyon/stations"
        response = await self.session.get(
            url,
            headers={"Content-Type": "application/vnd.bikes.v3+json"},
        )
        json = await response.json()
        print(json)
        return json

    async def get_station_bikes(self, stationNumber: int):
        url = f"https://api.cyclocity.fr/contracts/lyon/bikes?stationNumber={stationNumber}"

        response = await self.session.get(
            url,
            headers={"Content-Type": "application/vnd.bikes.v3+json"},
            params={"stationNumber": stationNumber}
        )
        json = await response.json()
        return json

    async def get_bikes(self):
        url = f"https://api.cyclocity.fr/contracts/lyon/bikes"

        response = await self.session.get(
            url,
            headers={"Content-Type": "application/vnd.bikes.v3+json"},
        )
        json = await response.json()
        return json


Api = VelovApi()
