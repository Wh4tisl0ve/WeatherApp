from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Locations
from .services.weather_api_service import WeatherApiService


weather_service = WeatherApiService()


@login_required(redirect_field_name=None)
def main_page(request):
    current_user = request.user
    id_user = current_user.id

    user_locations = Locations.objects.filter(users_id=id_user)
    user_locations_dto = [
        weather_service.get_location_by_coord(
            loc.latitude,
            loc.longitude,
        )
        for loc in user_locations
    ]
    # и передаем user_locations_dto в шаблон

    print(*weather_service.get_all_locations_by_name("Mos"), sep="\n")
    print(weather_service.get_location_by_name("Moscow"))

    return render(request, "weather/index.html")


@login_required(redirect_field_name=None)
def search_page(request):
    if request.method == "GET":
        params = request.GET
        location_name = params.get("name")

        if location_name:
            all_search_locations = weather_service.get_all_locations_by_name(
                location_name
            )

        return render(
            request, "weather/search.html", context={"location_name": location_name}
        )
