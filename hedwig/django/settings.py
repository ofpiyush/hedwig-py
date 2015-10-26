from django.conf import settings
from hedwig.core.settings import Settings, DEFAULTS
import os

USER_SETTINGS = getattr(settings, 'HEDWIG', None)
hedwig_settings = Settings(USER_SETTINGS, DEFAULTS)

project_name = os.getenv('DJANGO_SETTINGS_MODULE').split('.')[0]
