from django.db.utils import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user', password='password')

    def test_none_username(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_user(username=None, password='password')

        self.assertEqual(str(context.exception), "Логин не может быть пустым")

    def test_username_exists(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username='user', password='password')

    def test_username_max_length(self):
        max_length = 20
        username_length = User._meta.get_field('username').max_length

        self.assertEqual(max_length, username_length)
