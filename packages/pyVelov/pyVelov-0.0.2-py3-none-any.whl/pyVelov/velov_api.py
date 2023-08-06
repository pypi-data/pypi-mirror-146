import requests


class VelovApi:


    def __init__(self):
        self.session = requests.Session()
        self.refreshToken = None
        self.accessToken = None

        self.BASE_URL = "https://api.cyclocity.fr/"
        self.START_AUTH_URL = self.BASE_URL + "auth/environments/PRD/client_tokens"
        self.AUTH_DATA = {
            "code": "vls.web.lyon:PRD",
            "key": "c3d9f5c22a9157a7cc7fe0e38269573bdd2f13ec48f867360ecdcbd35b196f87"
        }

    def set_tokens(self):
        response = self.session.post(self.START_AUTH_URL, json=self.AUTH_DATA)
        response = response.json()
        self.refreshToken = response['refreshToken']
        self.accessToken = response["accessToken"]
        self.session.headers.update({"Authorization": f"Taknv1 {self.accessToken}"})

        print("Done getting tokens")

    def get_station(self, stationNumber: int):
        url = f"{self.BASE_URL}contracts/lyon/stations/{stationNumber}"
        response = self.session.get(
            url,
            headers={"Content-Type": "application/vnd.station.v4+json"}
        )
        return response.json()

    def get_stations(self):
        url = f"{self.BASE_URL}contracts/lyon/stations"
        response = self.session.get(
            url,
            headers={"Content-Type": "application/vnd.bikes.v3+json"},
        )
        json = response.json()

        return json

    def get_station_bikes(self, stationNumber: int):
        url = f"https://api.cyclocity.fr/contracts/lyon/bikes?stationNumber={stationNumber}"

        response = self.session.get(
            url,
            headers={"Content-Type": "application/vnd.bikes.v3+json"},
            params={"stationNumber": stationNumber}
        )
        json = response.json()
        return json

    def get_bikes(self):
        url = f"https://api.cyclocity.fr/contracts/lyon/bikes"

        response = self.session.get(
            url,
            headers={"Content-Type": "application/vnd.bikes.v3+json"},
        )
        json = response.json()
        return json


Api = VelovApi()

