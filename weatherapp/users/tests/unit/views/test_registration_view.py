from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class RegistrationViewTestClass(TestCase):

    def setUp(self):
        data = {
            'username': 'user1',
            'password1': 'password',
            'password2': 'password'
        }
        client = Client()
        client.post('/accounts/register/', data=data)

    def test_view_available(self):
        client = Client()
        response = client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_make_correct_registration(self):
        data = {
            'username': 'user2',
            'password1': 'password',
            'password2': 'password'
        }
        client = Client()
        response = client.post('/accounts/register/', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login/'))
