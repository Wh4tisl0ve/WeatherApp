from importlib import import_module

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone


class SessionMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        session_engine = import_module(settings.SESSION_ENGINE)
        self.SessionStore = session_engine.SessionStore

    def process_request(self, request):
        session_id_cookie = request.COOKIES.get("sessionid")
        request.session = self.SessionStore(session_id_cookie)

    def process_response(self, request, response):
        current_session = request.session.get()

        if current_session and current_session.expire_time > timezone.now():
            time_expire_session = (
                current_session.expire_time - timezone.now()
            ).total_seconds()
            response.set_cookie(
                "sessionid",
                current_session,
                max_age=time_expire_session,
                httponly=True,
            )
        else:
            response.delete_cookie("sessionid")

        return response
