from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import Locations
from .services.weather_api_service import WeatherApiService


class MainPageView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        current_user = request.user

        user_locations = Locations.objects.filter(user=current_user)
        user_locations_dto = []

        for loc in user_locations:
            location_dto = WeatherApiService.get_location_by_coord(loc.latitude, loc.longitude)

            location_dto.name = loc.name
            location_dto.country = loc.country

            user_locations_dto.append(location_dto)

        paginator = Paginator(user_locations_dto, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request, "weather/layouts/index.html", context={'page_obj': page_obj}
        )

    def post(self, request, *args, **kwargs):
        current_user = request.user
        latitude_request = float(request.POST.get("latitude"))
        longitude_request = float(request.POST.get("longitude"))

        location_entity = Locations.objects.filter(user=current_user).get(
            latitude=latitude_request,
            longitude=longitude_request,
        )

        location_entity.delete()
        return redirect("weather:main")


class SearchPageView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        params = request.GET
        location_name = params.get("name")

        if location_name:
            all_search_locations = WeatherApiService.get_all_locations_by_name(
                name=location_name
            )

            return render(
                request,
                "weather/layouts/search.html",
                context={
                    "location_name": location_name,
                    "locations": all_search_locations,
                },
            )

        return render(request, "weather/layouts/search.html")

    def post(self, request, *args, **kwargs) -> HttpResponse:
        current_user = request.user
        name = request.POST.get("name")
        country = request.POST.get("country")
        location_latitude = float(request.POST.get("latitude").replace(',', '.'))
        location_longitude = float(request.POST.get("longitude").replace(',', '.'))

        location_dto = WeatherApiService.get_location_by_coord(
            lat=location_latitude,
            lon=location_longitude,
        )

        location_entity = Locations(
            name=name,
            country=country,
            latitude=location_dto.latitude,
            longitude=location_dto.longitude,
            user=current_user,
        )

        location_entity.save()
        return redirect("weather:main")
