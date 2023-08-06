class Station:
    """
    Defines a Velo'v staion
    """

    def __init__(self, data: dict) -> None:
        self.id = data["id"]
        self.name = data["name"]
        self.number = data["number"]
        self.open = data["open"]
        self.updatedAt = data["updatedAt"]
        self.number_of_bikes = \
            data["availabilities"]["main"]["bikes"]["electrical"] \
            + data["availabilities"]["main"]["bikes"]["mechanical"]

        self.stands = data["availabilities"]["main"]["stands"]
        self.data = data



