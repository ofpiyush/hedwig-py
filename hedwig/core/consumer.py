import logging
from future.utils import iteritems

from pika.exceptions import ConnectionClosed

from hedwig import utils
from hedwig.core.base import Base

LOGGER = logging.getLogger(__name__)


class Consumer(Base):
    def __init__(self, settings):
        self._callbacks = {}
        super(Consumer, self).__init__(settings)

    def consume(self):
        """
        Consumes messages from RabbitMQ
        :return:
        :raises KeyboardInterrupt: if one was sent to it
        :raises Exception: if RAISE_EXCEPTION on CONSUMER is true
        """
        LOGGER.debug('Consumer Initialized')
        # self.connect()
        channel = self.get_channel()
        self._bind_things(channel)

        try:
            LOGGER.info('Start consuming')
            channel.start_consuming()
        except ConnectionClosed:
            LOGGER.exception('Pika connection closed detected. Will attempt to start consuming again')
            self.consume()
        except KeyboardInterrupt as e:
            LOGGER.info('Keyboard interrupt, stop consuming')
            self.shutdown()
            raise
        except Exception as e:
            LOGGER.exception("'%s" % str(e))
            self.shutdown()
            if self.settings.CONSUMER['RAISE_EXCEPTION']:
                LOGGER.info("CONSUMER RAISED EXCEPTION")
                raise

    def callback(self, func_string):
        """
        Wraps callback from settings

        :param func_string: string notation of actual callback to be called
        :return callback_wrapper: Callback wrapper
        :raises Exception: if consumer RAISE_EXCEPTION is true
        """
        def callback_wrapper(ch, method, properties, body):
            LOGGER.info("Got message - %s with body %s" % (method.routing_key, body))
            if func_string not in self._callbacks:
                self._callbacks[func_string] = utils.import_obj(func_string)
            try:
                self._callbacks[func_string](ch, method, properties, body)
            except Exception as e:
                LOGGER.exception("Callback exception '%s'" % str(e))
                if self.settings.CONSUMER['RAISE_EXCEPTION']:
                    LOGGER.info("CALLBACK RAISED EXCEPTION")
                    raise

        return callback_wrapper

    def _bind_things(self, channel):
        LOGGER.debug('Attempting to bind queues')
        for q_name, q_settings in iteritems(self.settings.CONSUMER['QUEUES']):
            LOGGER.debug('Declaring queue - %s' % q_name)
            channel.queue_declare(queue=q_name, durable=q_settings['DURABLE'], auto_delete=q_settings['AUTO_DELETE'])
            for binding in q_settings['BINDINGS']:
                LOGGER.info("Binding the queue - %s with key %s" % (q_name, binding))
                channel.queue_bind(exchange=self.settings.EXCHANGE, queue=q_name,
                                   routing_key=binding)
            LOGGER.debug("Setting Basic consume for callback - %s " % q_settings['CALLBACK'])
            channel.basic_consume(self.callback(q_settings['CALLBACK']), queue=q_name,
                                  no_ack=q_settings['NO_ACK'])

