from weather.dto import LocationWeatherDTO


class LocationWeatherMapper:
    @classmethod
    def dict_to_dto(cls, data: dict) -> LocationWeatherDTO:
        return LocationWeatherDTO(
            name=data.get("name"),
            country=data.get("sys", {}).get("country"),
            wind_speed=data.get("wind", {}).get("speed"),
            temp=round(data.get("main", {}).get("temp")),
            feels_like=round(data.get("main", {}).get("feels_like")),
            temp_min=round(data.get("main", {}).get("temp_min")),
            temp_max=round(data.get("main", {}).get("temp_max")),
            longitude=data.get("coord", {}).get("lon"),
            latitude=data.get("coord", {}).get("lat"),
            weather_description=data.get('weather', [{}])[0].get('description'),
            icon_name=data.get('weather', [{}])[0].get('icon'),
        )
