from django.conf import settings
from hedwig.core.settings import Settings, DEFAULTS

USER_SETTINGS = getattr(settings, 'HEDWIG', None)
hedwig_settings = Settings(USER_SETTINGS, DEFAULTS)
