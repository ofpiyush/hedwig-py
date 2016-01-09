__author__ = 'sandeep'
import multiprocessing

import logging

LOGGER = logging.getLogger(__name__)


class DjangoHedwigWorker(multiprocessing.Process):
    def __init__(self, *args, **kwargs):
        self.hedwig_consumer = None
        super(DjangoHedwigWorker, self).__init__(*args, **kwargs)

    def run(self):
        from hedwig.core.consumer import Consumer
        import django
        django.setup()
        from .settings import hedwig_settings
        self.hedwig_consumer = Consumer(hedwig_settings)
        LOGGER.info("Django Hedwig consumer: starting")
        self.hedwig_consumer.consume()
        LOGGER.info("Django hedwig consumer: stopped")

    def shutdown(self):
        LOGGER.info("Django Hedwig consumer: shutting down")
        if self.hedwig_consumer is not None:
            self.hedwig_consumer.shutdown()
        LOGGER.info("Django Hedwig consumer: shutdown complete")
