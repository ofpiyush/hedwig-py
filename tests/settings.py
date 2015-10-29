from hedwig.core.settings import Settings, DEFAULTS

USER_SETTINGS = {
    'VHOST': 'hedwig_server',
    'USERNAME': 'hedwig_test',
    'PASSWORD': 'hedwig_pass',
    'CONSUMER': {
        'QUEUES': {
            'everything_printer': {
                'BINDINGS': ['#'],
                'CALLBACK': 'tests.callbacks.printer',
                'DURABLE': False,
                'AUTO_DELETE': True,
                'NO_ACK': True
            },
            'accounts_catch_all': {
                'BINDINGS': ['accounts.#'],
                'CALLBACK': 'tests.callbacks.accounts_printer',
                'DURABLE': False,
                'AUTO_DELETE': True,
                'NO_ACK': True
            },
            'message_create': {
                'BINDINGS': ['message.serializer.create.*'],
                'CALLBACK': 'tests.callbacks.message_printer',
                'DURABLE': False,
                'AUTO_DELETE': True,
                'NO_ACK': True
            }
        }
    }
}

hedwig_settings = Settings(USER_SETTINGS, DEFAULTS)
