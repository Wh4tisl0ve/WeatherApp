from django.utils import timezone

from ..models import Session
from ..backend import SessionStore


def create_session(request, user):
    session = request.session
    user_session = Session.get_session_by_user(user)

    if user_session:
        request.session = SessionStore(user_session.session_key)
        session = request.session
        if user_session.expire_time < timezone.now():
            session.update(user)
    else:
        session.create(user)
