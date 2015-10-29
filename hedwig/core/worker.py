__author__ = 'sandeep'
import multiprocessing

from consumer import Consumer


class HedwigWorker(multiprocessing.Process):
    def __init__(self, settings, *args, **kwargs):
        self.hedwig_consumer = Consumer(settings)
        super(HedwigWorker, self).__init__(*args, **kwargs)

    def run(self):
        self.hedwig_consumer.consume()

    def shutdown(self):
        self.hedwig_consumer.shutdown()
