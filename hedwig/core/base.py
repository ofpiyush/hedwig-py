import pika


class Base(object):
    def __init__(self, settings):
        self.settings = settings
        credentials = pika.PlainCredentials(username=self.settings.USERNAME,
                                            password=self.settings.PASSWORD)
        self.conn_params = pika.ConnectionParameters(host=self.settings.HOST, port=self.settings.PORT,
                                                virtual_host=self.settings.VHOST, credentials=credentials,
                                                heartbeat_interval=self.settings.HEARTBEAT_INTERVAL,
                                                socket_timeout=self.settings.SOCKET_TIMEOUT)
        self.connection = None

    def create_channel(self):
        channel = self.connection.channel()
        channel.exchange_declare(exchange=self.settings.EXCHANGE, type=self.settings.EXCHANGE_TYPE, durable=True)
        return channel

    def connect(self):
        self.connection = pika.BlockingConnection(self.conn_params)

    def close_channel(self, channel):
        if channel.is_open:
            channel.cancel()
            channel.close()

    """
        Todo: Figure if we can call this method from __del__ without fucking everything over
    """
    def shutdown(self):
        self.connection.close()
        self.connection = None
