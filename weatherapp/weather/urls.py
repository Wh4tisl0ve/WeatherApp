from django.urls import path

from .views import MainView, SearchView, delete_location

urlpatterns = [
    path("", MainView.as_view(), name='main'),
    path("search/", SearchView.as_view(), name='search'),
    path("delete/location/<int:location_id>/",  delete_location, name="location-delete")
]
