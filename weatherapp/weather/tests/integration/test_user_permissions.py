from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.sessions.models import Session

from weather.views.views import MainPageView

User = get_user_model()


class UserPermissionTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.registered_user = User.objects.create_user(username='user', password='password')
        self.registered_user.save()

    def test_main_page_access_for_unauthenticated(self):
        request = self.factory.get(reverse('weather:main'))
        request.user = AnonymousUser()

        response = MainPageView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(request.user.is_authenticated, False)

    def test_main_page_access_for_authenticated(self):
        request = self.factory.get(reverse('weather:main'))
        request.user = self.registered_user

        response = MainPageView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.user.is_authenticated, True)

    def test_redirect_after_logout(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('weather:main'))

        self.assertEqual(response.status_code, 200)

        self.client.logout()

        response = self.client.get(reverse('weather:main'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/')

    def test_create_session(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('weather:main'))

        session_key = self.client.session.session_key

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Session.objects.get(session_key=session_key))