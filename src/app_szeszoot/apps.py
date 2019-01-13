from django.apps import AppConfig


class AppSzeszootConfig(AppConfig):
    name = 'app_szeszoot'

    def ready(self):
        import app_szeszoot.signals
