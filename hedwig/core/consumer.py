from importlib import import_module
import logging
from hedwig.core.base import Base

LOGGER = logging.getLogger(__name__)


class Consumer(Base):
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
        except KeyboardInterrupt as e:
            LOGGER.info('Keyboard interrupt, stop consuming')
            self.shutdown()
            raise e
        except Exception as e:
            LOGGER.exception("'%s" % str(e))
            self.shutdown()
            print self.settings.CONSUMER
            if self.settings.CONSUMER['RAISE_EXCEPTION']:
                LOGGER.info("CONSUMER RAISED EXCEPTION")
                raise e

    def callback(self, func):
        """
        Wraps callback from settings

        :param func: actual callback to be called
        :return callback_wrapper: Callback wrapper
        :raises Exception: if consumer RAISE_EXCEPTION is true
        """
        def callback_wrapper(ch, method, properties, body):
            LOGGER.info("Got message - %s with body %s" % (method.routing_key, body))
            try:
                func(ch, method, properties, body)
            except Exception as e:
                LOGGER.exception("Callback exception '%s'" % str(e))
                if self.settings.CONSUMER['RAISE_EXCEPTION']:
                    LOGGER.info("CALLBACK RAISED EXCEPTION")
                    raise e

        return callback_wrapper

    def _bind_things(self, channel):
        LOGGER.debug('Attempting to bind queues')
        for q_name, q_settings in self.settings.CONSUMER['QUEUES'].iteritems():
            LOGGER.debug('Declaring queue - %s' % q_name)
            channel.queue_declare(queue=q_name, durable=q_settings['DURABLE'], auto_delete=q_settings['AUTO_DELETE'])
            for binding in q_settings['BINDINGS']:
                LOGGER.info("Binding the queue - %s with key %s" % (q_name, binding))
                channel.queue_bind(exchange=self.settings.EXCHANGE, queue=q_name,
                                   routing_key=binding)
            LOGGER.debug("Setting Basic consume for callback - %s " % q_settings['CALLBACK'])
            channel.basic_consume(self.callback(self._import(q_settings['CALLBACK'])), queue=q_name,
                                  no_ack=q_settings['NO_ACK'])

    def _import(self, cb):
        LOGGER.debug("Attempting to import - %s" % cb)
        try:
            # Nod to DRF for nod to tastypie's use of importlib.
            parts = cb.split('.')
            module_path, callback_name = '.'.join(parts[:-1]), parts[-1]
            LOGGER.debug("Importing %s from %s" % (callback_name, module_path))
            module = import_module(module_path)
            return getattr(module, callback_name)
        except (ImportError, AttributeError) as e:
            msg = "Could not import '%s' %s: %s." % (cb, e.__class__.__name__, e)
            raise ImportError(msg)
