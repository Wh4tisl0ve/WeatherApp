import requests
from decouple import config

from weather.dto import LocationWeatherDTO
from weather.mappers import LocationWeatherMapper


class WeatherApiService:
    __SECRET_KEY = config("WEATHER_API_KEY")
    __api_get_one_location_v25 = "https://api.openweathermap.org/data/2.5/weather"
    __api_get_five_day_weather_v25 = "https://api.openweathermap.org/data/2.5/forecast"
    __api_find_all_locations_v10 = "https://api.openweathermap.org/geo/1.0/direct"

    @classmethod
    def get_all_locations_by_name(
            cls, name: str = "", limit: int = 10
    ) -> list[LocationWeatherDTO]:
        all_location_deserialize = requests.get(
            cls.__api_find_all_locations_v10,
            params={"q": name, "APPID": cls.__SECRET_KEY, "limit": limit, "lang": "ru"},
        ).json()

        return [
            LocationWeatherDTO(
                name=loc.get("name"),
                country=loc.get("country"),
                longitude=loc.get("lon"),
                latitude=loc.get("lat"),
            )
            for loc in all_location_deserialize
        ]

    @classmethod
    def get_location_by_coord(cls, lat: float, lon: float) -> LocationWeatherDTO:
        location_deserialize = requests.get(
            cls.__api_get_one_location_v25,
            params={
                "lat": lat,
                "lon": lon,
                "APPID": cls.__SECRET_KEY,
                "lang": "ru",
                "units": "metric",
            },
        ).json()

        return LocationWeatherMapper.dict_to_dto(location_deserialize)

    @classmethod
    def get_five_day_weather_forecast(cls, lat: float, lon: float):
        location_deserialize = requests.get(
            cls.__api_get_five_day_weather_v25,
            params={
                "lat": lat,
                "lon": lon,
                "APPID": cls.__SECRET_KEY,
                "lang": "ru",
                "units": "metric",
            },
        ).json()

        return LocationWeatherMapper.dict_to_dto(location_deserialize)
