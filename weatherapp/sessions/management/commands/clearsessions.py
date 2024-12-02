from importlib import import_module

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        session_engine = import_module(settings.SESSION_ENGINE)
        session_engine.SessionStore.clear_expired()
