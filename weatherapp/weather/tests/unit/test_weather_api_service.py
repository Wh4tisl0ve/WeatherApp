from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from weather.services.weather_api_service import WeatherApiService

User = get_user_model()


class WeatherServiceTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_user = User.objects.create_user(username='user', password='password')
