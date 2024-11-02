from django.urls import path

from .views import MainView, SearchView


urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path("search/", SearchView.as_view(), name="search"),
]
