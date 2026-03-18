from dataclasses import dataclass


@dataclass
class LocationData:
    Name: str


class Location:

    def __init__(self, data: LocationData):
        self.name = data.Name
