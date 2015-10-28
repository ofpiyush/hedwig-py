from django.apps.config import AppConfig
from .signals import register_hedwig_callbacks
from .settings import hedwig_settings


class HedwigAppConfig(AppConfig):
    name = 'hedwig.django'
    label = 'hedwig.django'

    def ready(self):
        if hedwig_settings.DJANGO['MODEL_SIGNALS']:
            register_hedwig_callbacks()
