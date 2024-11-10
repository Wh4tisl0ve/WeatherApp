from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_new_user(self):
        data = {
            'username': 'user',
            'password1': 'password',
            'password2': 'password',
        }
        response = self.client.post(reverse('users:register'), data=data)

        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.get(username='user'))
