__author__ = 'sandeep'
import multiprocessing

from consumer import Consumer

import logging

LOGGER = logging.getLogger(__name__)


class HedwigWorker(multiprocessing.Process):
    def __init__(self, settings, *args, **kwargs):
        self.hedwig_consumer = Consumer(settings)
        super(HedwigWorker, self).__init__(*args, **kwargs)

    def run(self):
        LOGGER.info("Hedwig consumer: starting")
        self.hedwig_consumer.consume()
        LOGGER.info("hedwig consumer: stopped")

    def shutdown(self):
        LOGGER.info("Hedwig consumer: shutting down")
        self.hedwig_consumer.shutdown()
        LOGGER.info("Hedwig consumer: shutdown complete")
