from .base import Base
import logging


class Emitter(Base):
    def emit(self, key, message):
        try:
            logging.debug("Hedwig: trying to emit - {0}".format(message))
            self.connect()
            pub_channel = self.create_channel()
            pub_channel.basic_publish(exchange=self.settings.EXCHANGE, routing_key=key, body=message)
            logging.info("Hedwig: Emitted - {0}".format(message))
            self.close_channel(pub_channel)
            self.shutdown()
        except Exception as e:
            logging.warning("Hedwig: Error - {0}".format(str(e)))
