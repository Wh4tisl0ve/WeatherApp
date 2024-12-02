from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate


User = get_user_model()


class AuthTestCase(TestCase):
    def test_exists_user_authenticate(self):
        User.objects.create_user(username="John", password="password")
        auth_user = authenticate(username="John", password="password")
        self.assertIsNotNone(auth_user)

    def test_not_exists_user_authenticate(self):
        User.objects.create_user(username="John", password="password")
        auth_user = authenticate(username="John", password="password1")
        self.assertIsNone(auth_user)
