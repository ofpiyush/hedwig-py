from .base import Base
import logging
from pika.exceptions import ConnectionClosed
LOGGER = logging.getLogger(__name__)


class Emitter(Base):
    def emit(self, key, message):
        try:
            self._emit(key, message)
        except ConnectionClosed:
            self.shutdown()
            self._emit(key, message)
        except Exception as e:
            LOGGER.exception("Emitter exception %s" % str(e))
            if self.settings.EMITTER['RAISE_EXCEPTION']:
                raise e

    def _emit(self, key, message):
        pub_channel = self.get_channel()
        LOGGER.debug("Trying to emit - %s" % message)
        pub_channel.basic_publish(exchange=self.settings.EXCHANGE, routing_key=key, body=message)
        logging.info("Emitted - %s" % message)

