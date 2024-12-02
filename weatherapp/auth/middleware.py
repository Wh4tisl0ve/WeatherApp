from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from django.utils.module_loading import import_string
from django.conf import settings


def load_backend(path):
    return import_string(path)()


def get_user_by_session_id(request):
    user = AnonymousUser()

    session = request.session.get()
    if session:
        auth_backend = load_backend(settings.AUTHENTICATION_BACKENDS[0])
        user = auth_backend.get_user(session.user_id)

    return user


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = get_user_by_session_id(request)
