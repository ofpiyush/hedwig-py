from hedwig.core.settings import Settings
from django.conf import settings

REST_FRAMEWORK_DEFAULTS = {
    'SERIALIZER_SIGNALS': True
}

HEDWIG_REST_FRAMEWORK_USER_SETTINGS = getattr(settings, 'HEDWIG_REST_FRAMEWORK', None)

hedwig_rest_framework_settings = Settings(HEDWIG_REST_FRAMEWORK_USER_SETTINGS, REST_FRAMEWORK_DEFAULTS)
