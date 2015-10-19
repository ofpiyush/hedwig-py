from hedwig.core.settings import Settings, DEFAULTS

USER_SETTINGS = {
    'VHOST': 'hedwig_server',
    'USERNAME': 'hedwig_test',
    'PASSWORD': 'hedwig_pass',
    'CONSUMER': {
        'QUEUES': {
            'accounts_catch_all': {
                'BINDINGS': ['accounts.#'],
                'CALLBACK': 'hedwig.tests.callbacks.accounts_printer',
                'DURABLE': False
            },
            'message_create': {
                'BINDINGS': ['message.serializer.create.*'],
                'CALLBACK': 'hedwig.tests.callbacks.message_printer',
                'DURABLE': False
            }
        }
    }
}

hedwig_settings = Settings(USER_SETTINGS, DEFAULTS)
