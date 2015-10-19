DEFAULTS = {
    'EXCHANGE': 'hedwig',
    'EXCHANGE_TYPE': 'topic',
    'HEARTBEAT_INTERVAL': 5,
    'SOCKET_TIMEOUT': 1,
    'HOST': 'localhost',
    'PORT': 5672,
    'VHOST': '',
    'USERNAME': '',
    'PASSWORD': '',

    'CONSUMER': {
        'QUEUES': {}
    }
}


# Nod to DRF for their settings

class Settings(object):
    """
    A settings object, that allows HEDWIG settings to be accessed as properties.
    """

    def __init__(self, user_settings=None, defaults=None):
        self.user_settings = user_settings or {}
        self.defaults = defaults or DEFAULTS

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid HEDWIG setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        setattr(self, attr, val)
        return val
