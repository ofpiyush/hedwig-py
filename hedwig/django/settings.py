import os

from django.conf import settings
from hedwig.core.settings import Settings, DEFAULTS

HEDWIG_USER_SETTINGS = getattr(settings, 'HEDWIG', None)
HEDWIG_DJANGO_USER_SETTINGS = getattr(settings, 'HEDWIG_DJANGO', None)


DJANGO_DEFAULTS = {
    'MODEL_SIGNALS': False,
    'HIDE_FIELDS': False,
    'NATURAL_PRIMARY_KEYS': True,
    'NATURAL_FOREIGN_KEYS': True
}

hedwig_settings = Settings(HEDWIG_USER_SETTINGS, DEFAULTS)
hedwig_django_settings = Settings(HEDWIG_DJANGO_USER_SETTINGS, DJANGO_DEFAULTS)

project_name = os.getenv('DJANGO_SETTINGS_MODULE').split('.')[0]


MODEL_DEFAULTS = {
    'fields': not bool(hedwig_django_settings.HIDE_FIELDS),
    'natural_primary_keys': bool(hedwig_django_settings.NATURAL_PRIMARY_KEYS),
    'natural_foreign_keys': bool(hedwig_django_settings.NATURAL_FOREIGN_KEYS),
    'created': True,
    'updated': True,
    'deleted': True
}
