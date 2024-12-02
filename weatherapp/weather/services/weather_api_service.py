import requests

from django.conf import settings

from weather.dto import LocationWeatherDTO
from .mappers import LocationWeatherMapper
from ..exceptions import OpenWeatherApiError


class WeatherApiService:
    __SECRET_KEY = settings.WEATHER_API_KEY
    __api_get_one_location_v25 = "https://api.openweathermap.org/data/2.5/weather"
    __api_find_all_locations_v10 = "https://api.openweathermap.org/geo/1.0/direct"

    @classmethod
    def check_response_error(cls, data_response_api):
        if "cod" in data_response_api and "message" in data_response_api:
            raise OpenWeatherApiError(
                data_response_api.get("cod", 500),
                data_response_api.get("message", "Unexpected Error"),
            )

    @classmethod
    def get_all_locations_by_name(
        cls, name: str = "", limit: int = 10
    ) -> list[LocationWeatherDTO]:
        all_location_deserialize = requests.get(
            cls.__api_find_all_locations_v10,
            params={"q": name, "APPID": cls.__SECRET_KEY, "limit": limit, "lang": "ru"},
        ).json()

        cls.check_response_error(all_location_deserialize)

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

        cls.check_response_error(location_deserialize)

        return LocationWeatherMapper.dict_to_dto(location_deserialize)
