__author__ = 'piyush'
from django.apps.config import AppConfig
from .signals import register_hedwig_callbacks

class HedwigAppConfig(AppConfig):
    name='hedwig'

    def ready(self):
        register_hedwig_callbacks()
