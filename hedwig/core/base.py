import pika
import logging


class Base(object):
    def __init__(self, settings):
        logging.info("Hedwig: Base init for class - {0}".format(self.__class__.__name__))
        self.settings = settings
        logging.debug("Hedwig: Setting credentials")
        credentials = pika.PlainCredentials(username=self.settings.USERNAME,
                                            password=self.settings.PASSWORD)
        logging.debug("Hedwig: Setting Connection params")
        self.conn_params = pika.ConnectionParameters(host=self.settings.HOST, port=self.settings.PORT,
                                                     virtual_host=self.settings.VHOST, credentials=credentials,
                                                     heartbeat_interval=self.settings.HEARTBEAT_INTERVAL,
                                                     socket_timeout=self.settings.SOCKET_TIMEOUT)

        self.connection = None

    def create_channel(self):
        logging.debug("Hedwig: Creating a channel")
        channel = self.connection.channel()
        logging.debug(
            "Hedwig: Declaring {0} exchange - {1}".format(self.settings.EXCHANGE_TYPE, self.settings.EXCHANGE)
        )
        channel.exchange_declare(exchange=self.settings.EXCHANGE, type=self.settings.EXCHANGE_TYPE, durable=True)
        return channel

    def connect(self):
        logging.debug("Hedwig: Making a blocking connection")
        if self.connection is None or not self.connection.is_open:
            self.connection = pika.BlockingConnection(self.conn_params)

    def close_channel(self, channel):
        logging.debug("Hedwig: Trying to close channel if open")
        if channel.is_open:
            logging.debug("Hedwig: Closing channel")
            channel.cancel()
            channel.close()

    def shutdown(self):
        if self.connection and self.connection.is_open:
            logging.debug("Hediwg: Shutdown called")
            self.connection.close()
