from __future__ import absolute_import
from hedwig.core.consumer import Consumer
from hedwig.django.settings import hedwig_settings
import threading

# Test to run hedwig consumer from within django


def start_consumer():
    consumer = Consumer(hedwig_settings)
    consumer.consume()


t = threading.Thread(target=start_consumer, args=(), kwargs={})
t.setDaemon(True)
t.start()
