import requests
from decouple import config

from weather.dto import LocationDTO


class WeatherApiService:
    __SECRET_KEY = config("WEATHER_API_KEY")
    __api_25 = "http://api.openweathermap.org/data/2.5/weather"
    __api_10 = "http://api.openweathermap.org/geo/1.0/direct"

    @classmethod
    def dict_to_dto(cls, location_dict: dict) -> LocationDTO:
        return LocationDTO(
            name=location_dict.get("name"),
            country=location_dict.get("sys", {}).get("country"),
            wind_speed=location_dict.get("wind", {}).get("speed"),
            temp=location_dict.get("main", {}).get("temp"),
            temp_min=location_dict.get("main", {}).get("temp_min"),
            temp_max=location_dict.get("main", {}).get("temp_max"),
            longitude=location_dict.get("coord", {}).get("lon"),
            latitude=location_dict.get("coord", {}).get("lat"),
        )

    @classmethod
    def get_all_locations_by_name(
            cls, name: str = "", limit: int = 10
    ) -> list[LocationDTO]:
        all_location_deserialize = requests.get(
            cls.__api_10,
            params={"q": name, "APPID": cls.__SECRET_KEY, "limit": limit, "lang": "ru"},
        ).json()

        return [
            LocationDTO(
                name=loc.get("name"),
                country=loc.get("country"),
                longitude=loc.get("lon"),
                latitude=loc.get("lat"),
            )
            for loc in all_location_deserialize
        ]

    @classmethod
    def get_location_by_coord(cls, lat: float, lon: float) -> LocationDTO:
        location_deserialize = requests.get(
            cls.__api_25,
            params={
                "lat": lat,
                "lon": lon,
                "APPID": cls.__SECRET_KEY,
                "lang": "ru",
                "units": "metric",
            },
        ).json()

        return cls.dict_to_dto(location_deserialize)

    @classmethod
    def get_location_by_name(cls, name: str = ""):
        location_deserialize = requests.get(
            cls.__api_25,
            params={
                "q": name,
                "APPID": cls.__SECRET_KEY,
                "lang": "ru",
                "units": "metric",
            },
        ).json()

        return cls.dict_to_dto(location_deserialize)
