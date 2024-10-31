import requests
from decouple import config


SECRET_KEY = config("WEATHER_API_KEY")
api_25 = "http://api.openweathermap.org/data/2.5/weather"
api_10 = "http://api.openweathermap.org/geo/1.0/direct"


def get_all_locations_by_name(name: str = ""):
    all_location_deserialize = requests.get(
        api_10, params={"q": name, 
                        "APPID": SECRET_KEY, 
                        "limit": 10, 
                        "lang": "ru"}
    ).json()

    return all_location_deserialize


def get_location_by_coord(lat: float, lon: float):
    location_deserialize = requests.get(
        api_25,
        params={
            "lat": lat,
            "lon": lon,
            "APPID": SECRET_KEY,
            "lang": "ru",
            "units": "metric",
        },
    ).json()

    return location_deserialize

def get_location_by_name(name: str = ""):
    location_deserialize = requests.get(
        api_25,
        params={
            "name": name,
            "APPID": SECRET_KEY,
            "lang": "ru",
            "units": "metric",
        },
    ).json()

    return location_deserialize
