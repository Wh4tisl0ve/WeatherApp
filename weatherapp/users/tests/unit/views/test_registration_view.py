from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class RegistrationViewTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(username='user1', password='password').save()

    def test_view_available(self):
        client = Client()
        response = client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_correct_registration(self):
        data = {
            'username': 'user2',
            'password1': 'password',
            'password2': 'password'
        }
        client = Client()
        response = client.post(reverse('users:register'), data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))

    def test_user_already_exists(self):
        data = {
            'username': 'user1',
            'password1': 'password',
            'password2': 'password',
        }

        client = Client()
        response = client.post(reverse('users:register'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_passwords_not_match(self):
        data = {
            'username': 'user6',
            'password1': 'password2',
            'password2': 'password',
        }

        client = Client()
        response = client.post(reverse('users:register'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_empty_data(self):
        data = {
            'username': '',
            'password1': '',
            'password2': '',
        }

        client = Client()
        response = client.post(reverse('users:register'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_russian_letter_username(self):
        data = {
            'username': 'Пользователь',
            'password1': 'password',
            'password2': 'password',
        }

        client = Client()
        response = client.post(reverse('users:register'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_password_min_length(self):
        data = {
            'username': 'user7',
            'password1': 'p' * 3,
            'password2': 'p' * 3,
        }

        client = Client()
        response = client.post(reverse('users:register'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_password_max_length(self):
        data = {
            'username': 'user7',
            'password1': 'p' * 50,
            'password2': 'p' * 50,
        }

        client = Client()
        response = client.post(reverse('users:register'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
