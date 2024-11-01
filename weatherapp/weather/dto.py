from dataclasses import dataclass

@dataclass(frozen=True)
class LocationDTO:
    name: str
    country: str
    wind_speed: float
    temp: float
    temp_min: float
    temp_max: float
    longitude: float
    latitude: float
