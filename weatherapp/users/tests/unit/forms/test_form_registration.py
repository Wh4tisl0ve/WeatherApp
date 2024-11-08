from django.test import TestCase
from django.contrib.auth import get_user_model

from users.forms import UserCreationForm

User = get_user_model()


class RegistrationFormTestClass(TestCase):
    def setUp(self):
        data = {
            'username': 'test',
            'password1': 'password',
            'password2': 'password',
        }
        registration_form = UserCreationForm(data=data)
        registration_form.save(commit=True)

    def test_form_is_valid(self):
        data = {
            'username': 'test2',
            'password1': 'password',
            'password2': 'password',
        }
        registration_form = UserCreationForm(data=data)
        self.assertTrue(registration_form.is_valid())

    def test_passwords_not_match(self):
        data = {
            'username': 'test2',
            'password1': 'password',
            'password2': 'password1',
        }
        registration_form = UserCreationForm(data=data)
        self.assertFalse(registration_form.is_valid())

    def test_password_min_length(self):
        data = {
            'username': 'test2',
            'password1': 'pas',
            'password2': 'pas',
        }
        registration_form = UserCreationForm(data=data)
        self.assertFalse(registration_form.is_valid())

    def test_password_max_length(self):
        data = {
            'username': 'test2',
            'password1': 'pas' * 30,
            'password2': 'pas' * 30,
        }
        registration_form = UserCreationForm(data=data)
        self.assertFalse(registration_form.is_valid())

    def test_username_russian_letter(self):
        data = {
            'username': 'абвгда',
            'password1': 'password',
            'password2': 'password',
        }
        registration_form = UserCreationForm(data=data)
        self.assertFalse(registration_form.is_valid())

    def test_username_already_exists(self):
        data = {
            'username': 'test',
            'password1': 'password',
            'password2': 'password',
        }
        registration_form = UserCreationForm(data=data)
        self.assertFalse(registration_form.is_valid())


