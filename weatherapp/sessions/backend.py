import string
import random

from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.utils.functional import cached_property


class SessionStore:
    def __init__(self, session_key=None):
        self._session_key = session_key
        self._session = {}

    @classmethod
    def get_model_class(cls):
        from .models import Session

        return Session

    @cached_property
    def model(self):
        return self.get_model_class()

    def __getitem__(self, key):
        return self._session[key]

    def __setitem__(self, key, value):
        self._session[key] = value

    def update(self, user):
        current_session = self.get()
        self._session_key = None

        if not current_session:
            current_session = self.get_session_by_user(user)

        current_session.delete()
        self.create(user)

    def create(self, user=None):
        self._session_key = None
        if user:
            session = self.create_model_instance(user)
            session.save()

    def flush(self, session_key=None):
        if session_key is None:
            if self._session_key is None:
                return
            session_key = self._session_key
        try:
            self.model.objects.get(session_key=session_key).delete()
        except self.model.DoesNotExist:
            pass

    def get(self):
        try:
            return self.model.objects.get(session_key=self._session_key)
        except self.model.DoesNotExist:
            pass

    def create_model_instance(self, user):
        return self.model(
            session_key=self.get_or_create_session_key(),
            user=user,
            expire_time=self.get_expire_time(),
        )

    def get_expire_time(self):
        now = timezone.now()
        time_session_activate = getattr(settings, "SESSION_COOKIE_AGE", 3600)
        expire_time = now + timedelta(seconds=time_session_activate)
        return expire_time

    def get_or_create_session_key(self):
        if self._session_key is None:
            self._session_key = self.get_new_session_key()
        return self._session_key

    def get_new_session_key(self):
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=40))

    def is_empty(self):
        return not self._session_key

    @classmethod
    def clear_expired(cls):
        cls.get_model_class().objects.filter(expire_time__lt=timezone.now()).delete()
