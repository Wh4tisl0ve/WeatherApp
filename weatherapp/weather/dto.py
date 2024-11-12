from dataclasses import dataclass


@dataclass
class LocationWeatherDTO:
    name: str = None
    country: str = None
    wind_speed: float = None
    temp: int = None
    feels_like: int = None
    temp_min: int = None
    temp_max: int = None
    longitude: float = None
    latitude: float = None
    weather_description: str = None
    icon_name: str = None
