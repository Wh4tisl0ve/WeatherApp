from unittest.mock import Mock, patch
from django.test import TestCase

from weather.dto import LocationDTO
from weather.services.weather_api_service import WeatherApiService


class WeatherServiceTestCase(TestCase):
    @patch('weather.services.weather_api_service.requests.get')
    def test_get_location_by_name(self, mock_requests):
        mock_response = Mock()
        mock_response.json.return_value = {
            "coord": {"lon": 37.6156, "lat": 55.752},
            "main": {
                "temp": 1.07,
                "temp_min": -1.06,
                "temp_max": 2.04
            },
            "wind": {
                "speed": 1.58,
                "deg": 336,
                "gust": 3.19
            },
            "sys": {"country": "RU"},
            "name": "Москва",
        }
        mock_requests.return_value = mock_response

        location_dto = WeatherApiService.get_location_by_name('Москва')
        self.assertIsInstance(location_dto, LocationDTO)
        self.assertEqual(location_dto.name, 'Москва')
        self.assertEqual(location_dto.country, 'RU')
        self.assertEqual(location_dto.latitude, 55.752)
        self.assertEqual(location_dto.longitude, 37.6156)
