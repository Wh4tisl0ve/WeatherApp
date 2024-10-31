from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Locations
from .services import get_all_locations_by_name



@login_required(redirect_field_name=None)
def main_page(request):
    current_user = request.user
    id_user = current_user.id

    user_locations_coord = Locations.objects.filter(users_id=id_user)

    return render(request, "weather/index.html")


@login_required(redirect_field_name=None)
def search_page(request):
    if request.method == "GET":
        params = request.GET
        location_name = params.get("name")

        if location_name:
            get_all_locations_by_name(location_name)

        return render(
            request, "weather/search.html", context={"location_name": location_name}
        )