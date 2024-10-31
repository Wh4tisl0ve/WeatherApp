from django.urls import path

from .views import main_page, search_page

urlpatterns = [
    path("", main_page, name='main'),
    path("search/", search_page, name='search'),
]
