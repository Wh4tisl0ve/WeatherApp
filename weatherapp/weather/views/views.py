from decimal import Decimal

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from weather.models import Locations
from weather.services.weather_api_service import WeatherApiService


class MainPageView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        current_user = request.user

        user_locations = Locations.objects.filter(user=current_user)
        user_locations_dto = []

        for loc in user_locations:
            location_dto = WeatherApiService.get_location_by_coord(
                loc.latitude, loc.longitude
            )

            location_dto.name = loc.name
            location_dto.country = loc.country

            user_locations_dto.append(location_dto)

        paginator = Paginator(user_locations_dto, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request, "weather/layouts/index.html", context={"page_obj": page_obj}
        )

    def post(self, request):
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
    def get(self, request) -> HttpResponse:
        current_user = request.user
        params = request.GET
        location_name = params.get("name")

        if location_name:
            all_search_locations = WeatherApiService.get_all_locations_by_name(
                name=location_name
            )

            existing_locations = Locations.objects.filter(
                user=current_user
            ).values_list("latitude", "longitude")

            unique_loc_dto = [
                loc_dto
                for loc_dto in all_search_locations
                if (
                    round(Decimal(loc_dto.latitude), 4),
                    round(Decimal(loc_dto.longitude), 4),
                )
                not in existing_locations
            ]

            return render(
                request,
                "weather/layouts/search.html",
                context={
                    "location_name": location_name,
                    "locations": unique_loc_dto,
                },
            )

        return render(request, "weather/layouts/search.html")

    def post(self, request) -> HttpResponse:
        current_user = request.user
        name = request.POST.get("name")
        country = request.POST.get("country")
        location_latitude = float(request.POST.get("latitude").replace(",", "."))
        location_longitude = float(request.POST.get("longitude").replace(",", "."))

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
