from dataclasses import dataclass


@dataclass
class LocationDTO:
    name: str = None
    country: str = None
    wind_speed: float = None
    temp: float = None
    temp_min: float = None
    temp_max: float = None
    longitude: float = None
    latitude: float = None
