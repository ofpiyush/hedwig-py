from django.apps.config import AppConfig
from .signals import register_hedwig_callbacks
from .settings import hedwig_django_settings


class HedwigAppConfig(AppConfig):
    name = 'hedwig.django'
    label = 'hedwig.django'

    def ready(self):
        if hedwig_django_settings.MODEL_SIGNALS:
            register_hedwig_callbacks()
