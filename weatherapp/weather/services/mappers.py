from weather.dto import LocationWeatherDTO


class LocationWeatherMapper:
    @classmethod
    def dict_to_dto(cls, data: dict) -> LocationWeatherDTO:
        return LocationWeatherDTO(
            name=data.get("name"),
            country=data.get("sys", {}).get("country"),
            wind_speed=data.get("wind", {}).get("speed"),
            temp=round(data.get("main", {}).get("temp", 0.0)),
            feels_like=round(data.get("main", {}).get("feels_like", 0.0)),
            temp_min=round(data.get("main", {}).get("temp_min", 0.0)),
            temp_max=round(data.get("main", {}).get("temp_max", 0.0)),
            longitude=data.get("coord", {}).get("lon"),
            latitude=data.get("coord", {}).get("lat"),
            weather_description=data.get('weather', [{}])[0].get('description'),
            icon_name=data.get('weather', [{}])[0].get('icon'),
        )
