from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Locations
from .services.weather_api_service import WeatherApiService


weather_service = WeatherApiService()


class MainView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwagrs):
        current_user = request.user

        user_locations = Locations.objects.filter(users=current_user)
        user_locations_dto = [
            weather_service.get_location_by_coord(loc.latitude, loc.longitude)
            for loc in user_locations
        ]

        return render(
            request, "weather/index.html", context={"locations": user_locations_dto}
        )

    def post(self, request, *args, **kwargs):
        current_user = request.user
        latitude_request = float(request.POST.get("latitude"))
        longitude_request = float(request.POST.get("longitude"))

        location_entity = Locations.objects.filter(users=current_user).get(
            latitude=latitude_request,
            longitude=longitude_request,
        )

        location_entity.delete()
        return redirect('main')


class SearchView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwagrs) -> HttpResponse:
        params = request.GET
        location_name = params.get("name")

        if location_name:
            all_search_locations = weather_service.get_all_locations_by_name(
                name=location_name
            )

            return render(
                request,
                "weather/search.html",
                context={
                    "location_name": location_name,
                    "locations": all_search_locations,
                },
            )
        else:
            return render(request, "weather/search.html")

    def post(self, request, *args, **kwargs) -> HttpResponse:
        current_user = request.user
        location_latitude = float(request.POST.get("latitude"))
        location_longitude = float(request.POST.get("longitude"))

        location_dto = weather_service.get_location_by_coord(
            lat=location_latitude,
            lon=location_longitude,
        )

        location_entity = Locations(
            name=location_dto.name,
            latitude=location_dto.latitude,
            longitude=location_dto.longitude,
            users=current_user,
        )

        location_entity.save()
        return redirect('main')
