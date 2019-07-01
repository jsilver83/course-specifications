from django.apps import AppConfig
from django.dispatch import Signal
from django.contrib.auth import user_logged_in


class MainAppConfig(AppConfig):
    name = 'main_app'

    def ready(self):
        import main_app.signals
