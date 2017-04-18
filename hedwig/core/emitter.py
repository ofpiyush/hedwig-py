from .base import Base
import logging
from pika.exceptions import ConnectionClosed
LOGGER = logging.getLogger(__name__)


class Emitter(Base):
    def emit(self, key, message):
        """
         Emits a message to RabbitMQ

        :param key: Routing key to emit on
        :param message: json serialized msg body
        :return:
        :raises Exception: If RAISE_EXCEPTION is true in emitter settings
        """
        try:
            self._emit(key, message)
        except ConnectionClosed:
            self.shutdown()
            self._emit(key, message)
        except Exception as e:
            LOGGER.exception("Emitter exception %s" % str(e))
            if self.settings.EMITTER['RAISE_EXCEPTION']:
                raise

    def _emit(self, key, message):
        pub_channel = self.get_channel()
        LOGGER.debug("Trying to emit - %s" % message)
        if pub_channel.basic_publish(exchange=self.settings.EXCHANGE, routing_key=key, body=message):
            LOGGER.info("Emitted - %s" % message)
        else:
            LOGGER.error("Failed to emit - %s" % message)
