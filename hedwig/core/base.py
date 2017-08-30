import pika
import logging
from pika.exceptions import ConnectionClosed

LOGGER = logging.getLogger(__name__)


class Base(object):
    def __init__(self, settings):
        LOGGER.info("Base init for class - {0}".format(self.__class__.__name__))
        self.settings = settings
        LOGGER.debug("Setting credentials")
        credentials = pika.PlainCredentials(username=self.settings.USERNAME,
                                            password=self.settings.PASSWORD)
        LOGGER.debug("Setting Connection params")
        self.conn_params = pika.ConnectionParameters(host=self.settings.HOST, port=self.settings.PORT,
                                                     virtual_host=self.settings.VHOST, credentials=credentials,
                                                     heartbeat_interval=self.settings.HEARTBEAT_INTERVAL,
                                                     socket_timeout=self.settings.SOCKET_TIMEOUT)

        self.connection = None
        self.channel = None

    def create_channel(self):
        LOGGER.debug("Creating a channel")
        channel = self.connection.channel()
        LOGGER.debug(
            "Declaring {0} exchange - {1}".format(self.settings.EXCHANGE_TYPE, self.settings.EXCHANGE)
        )
        channel.exchange_declare(exchange=self.settings.EXCHANGE, exchange_type=self.settings.EXCHANGE_TYPE, durable=True)
        return channel

    def get_channel(self):

        self.connect()
        if self.channel is None or not self.channel.is_open:
            LOGGER.info("No active channel found, creating a channel")
            self.channel = self.create_channel()
        return self.channel

    def connect(self):
        LOGGER.debug("Making a blocking connection")
        if self.connection is None or not self.connection.is_open:
            LOGGER.info("No active connection found, creating a connection")
            self.connection = pika.BlockingConnection(self.conn_params)

    def close_channel(self):
        LOGGER.debug("Trying to close channel if open")
        if self.channel and self.channel.is_open:
            LOGGER.debug("Closing channel")
            try:
                self.channel.cancel()
                self.channel.close()
            except ConnectionClosed:
                self.channel = None

    def shutdown(self):
        LOGGER.info("Shutdown called")
        self.close_channel()
        if self.connection and self.connection.is_open:
            LOGGER.info("Closing connection")
            try:
                self.connection.close()
            except ConnectionClosed:
                self.connection = None
