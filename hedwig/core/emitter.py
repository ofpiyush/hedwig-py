from .base import Base
import logging
LOGGER = logging.getLogger(__name__)


class Emitter(Base):
    def emit(self, key, message):
        try:
            LOGGER.debug("Trying to emit - %s" % message)
            self.connect()
            pub_channel = self.create_channel()
            pub_channel.basic_publish(exchange=self.settings.EXCHANGE, routing_key=key, body=message)
            logging.info("Emitted - %s" % message)
            self.close_channel(pub_channel)
            self.shutdown()
        except Exception as e:
            LOGGER.exception("Emitter exception %s" % str(e))
            if self.settings.EMITTER['RAISE_EXCEPTION']:
                raise e
