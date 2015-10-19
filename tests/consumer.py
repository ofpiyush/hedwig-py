from hedwig.core.consumer import Consumer
from settings import hedwig_settings

hedwig_consumer = Consumer(hedwig_settings)
hedwig_consumer.consume()
