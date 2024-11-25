from django.contrib.auth import get_user_model
from importlib import import_module
from django.conf import settings

UserModel = get_user_model()
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


def login(request, user):
    pass


def logout(request):
    request.session.flush()
    if hasattr(request, "user"):
        from django.contrib.auth.models import AnonymousUser

        request.user = AnonymousUser()
