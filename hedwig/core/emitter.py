from .base import Base


class Emitter(Base):

    def emit(self, key, message):
        pub_channel = self.create_channel()
        pub_channel.basic_publish(exchange=self.settings.EXCHANGE, routing_key=key, body=message)
        self.close_channel(pub_channel)

