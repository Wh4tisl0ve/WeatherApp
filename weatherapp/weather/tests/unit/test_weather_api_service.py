from unittest.mock import Mock, patch
from django.test import TestCase

from weather.dto import LocationDTO
from weather.services.weather_api_service import WeatherApiService


class WeatherServiceTestCase(TestCase):
    def setUp(self):
        self.location_data = {
            "coord": {"lon": 37.6156, "lat": 55.752},
            "main": {"temp": 1.07, "temp_min": -1.06, "temp_max": 2.04},
            "wind": {"speed": 1.58, "deg": 336, "gust": 3.19},
            "sys": {"country": "RU"},
            "name": "Москва",
        }

    @patch('weather.services.weather_api_service.requests.get')
    def test_get_location_by_name(self, mock_requests):
        mock_response = Mock()
        mock_response.json.return_value = self.location_data
        mock_requests.return_value = mock_response

        location_dto = WeatherApiService.get_location_by_name('Москва')
        self.assertIsInstance(location_dto, LocationDTO)
        self.assertEqual(location_dto.name, 'Москва')
        self.assertEqual(location_dto.country, 'RU')
        self.assertEqual(location_dto.latitude, 55.752)
        self.assertEqual(location_dto.longitude, 37.6156)

    @patch('weather.services.weather_api_service.requests.get')
    def test_get_location_by_coord(self, mock_requests):
        mock_response = Mock()
        mock_response.json.return_value = self.location_data
        mock_requests.return_value = mock_response

        location_dto = WeatherApiService.get_location_by_coord(lat=55.752, lon=37.6156)
        self.assertIsInstance(location_dto, LocationDTO)
        self.assertEqual(location_dto.name, 'Москва')
        self.assertEqual(location_dto.country, 'RU')
        self.assertEqual(location_dto.latitude, 55.752)
        self.assertEqual(location_dto.longitude, 37.6156)

    @patch.object(WeatherApiService, 'get_location_by_name')
    def test_get_all_locations_by_name(self, mock_get_location_by_coord):
        mock_get_location_by_coord.return_value = [
            LocationDTO(name="Moscow",
                        latitude=55.7504461,
                        longitude=37.6174943,
                        country="RU"),
            LocationDTO(name="Moscow",
                        latitude=55.7504461,
                        longitude=37.6174943,
                        country="RU"),
        ]

        locations_dto = WeatherApiService.get_all_locations_by_name(name='Москва', limit=2)
        self.assertIsInstance(locations_dto, list)
        self.assertEqual(len(locations_dto), 2)
