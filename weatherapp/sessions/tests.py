import time

from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.conf import settings

from .models import Session
from .backend import SessionStore
from .services.session_service import create_session

User = get_user_model()


class SessionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User.objects.create_user(username="John", password="password")
        User.objects.create_user(username="Bob", password="password")

    def test_session_created(self):
        request = HttpRequest()
        user = User.objects.get(username="John")

        request.user = user
        request.session = SessionStore()
        create_session(request, user)

        created_session = Session.get_session_by_user(user)
        self.assertIsNotNone(created_session)

    def test_expired_time(self):
        settings.SESSION_COOKIE_AGE = 1

        request = HttpRequest()
        user = User.objects.get(username="John")

        request.user = user
        request.session = SessionStore()
        create_session(request, user)

        user_session = Session.get_session_by_user(user)
        self.assertIsNotNone(user_session)

        time.sleep(2)
        SessionStore.clear_expired()

        user_session = Session.get_session_by_user(user)
        self.assertIsNone(user_session)

    def test_many_sessions_for_different_user(self):
        request1 = HttpRequest()
        request2 = HttpRequest()

        user1 = User.objects.get(username="John")
        user2 = User.objects.get(username="Bob")

        request1.user = user1
        request1.session = SessionStore()

        request2.user = user2
        request2.session = SessionStore()

        create_session(request1, user1)
        create_session(request2, user2)

        created_session1 = Session.get_session_by_user(user1)
        created_session2 = Session.get_session_by_user(user2)

        self.assertIsNotNone(created_session1)
        self.assertIsNotNone(created_session2)
        self.assertNotEqual(created_session1.session_key, created_session2.session_key)

    def test_update_session(self):
        settings.SESSION_COOKIE_AGE = 1
        user = User.objects.get(username="John")

        request1 = HttpRequest()
        request2 = HttpRequest()

        request1.user = user
        request1.session = SessionStore()

        request2.user = user
        request2.session = SessionStore()

        create_session(request1, user)
        created_session1 = Session.get_session_by_user(user)
        self.assertIsNotNone(created_session1)

        time.sleep(2)

        create_session(request2, user)
        created_session2 = Session.get_session_by_user(user)
        self.assertIsNotNone(created_session2)

        self.assertNotEqual(created_session1.session_key, created_session2.session_key)

    def test_use_active_session(self):
        user = User.objects.get(username="John")

        request1 = HttpRequest()
        request2 = HttpRequest()

        request1.user = user
        request1.session = SessionStore()

        request2.user = user
        request2.session = SessionStore()

        create_session(request1, user)
        created_session1 = Session.get_session_by_user(user)
        self.assertIsNotNone(created_session1)

        create_session(request2, user)
        created_session2 = Session.get_session_by_user(user)
        self.assertIsNotNone(created_session2)

        self.assertEqual(created_session1.session_key, created_session2.session_key)
