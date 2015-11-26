from copy import deepcopy

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
    'EMITTER': {
        'RAISE_EXCEPTION': False,
    },
    'CONSUMER': {
        'RAISE_EXCEPTION': False,
        'QUEUES': {}
    }
}

# Nod to https://www.xormedia.com/recursively-merge-dictionaries-in-python/


def dict_merge(a, b):
    """recursively merges dict's. not just simple a['key'] = b['key'], if
    both a and bhave a key who's value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary."""
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
                result[k] = dict_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result


# Nod to DRF for their settings, added dict_merge with deep copy to make it work with our use case

class Settings(object):
    """
    A settings object, that allows HEDWIG settings to be accessed as properties.
    """

    def __init__(self, user_settings=None, defaults=None):
        self.user_settings = user_settings or {}
        self.defaults = defaults or DEFAULTS
        if isinstance(self.user_settings, dict):
            self.user_settings = dict_merge(self.defaults, self.user_settings)
        else:
            raise TypeError("Expected settings to be a dict")

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

    def __getitem__(self, item):
        return getattr(self, item)
