from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class AuthorizationViewTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='user', password='password').save()

    def test_view_available(self):
        client = Client()
        response = client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_correct_authorization(self):
        data = {
            'username': 'user',
            'password': 'password',
        }
        client = Client()
        response = client.post(reverse('users:login'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('weather:main'))
