import logging
import inspect
from future.utils import iteritems

from pika.exceptions import ConnectionClosed

from hedwig import utils
from hedwig.core.base import Base
from hedwig.core.settings import DEFAULT_QUEUE_SETTINGS

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

    def callback(self, func):
        """
        Wraps callback from settings

        :param func: function or string notation of actual callback to be called
        :return callback_wrapper: Callback wrapper
        :raises Exception: if consumer RAISE_EXCEPTION is true
        """
        if callable(func):
            mod = inspect.getmodule(func)
            if mod is None:
                raise Exception("Can't determine module for - %s" % (func.__name__))
            func_string = "{}.{}.{}.{}".format(
                "__hedwig",
                mod.__name__,
                getattr(func.__class__, "__name__", "function"),
                func.__name__
            )
            self._callbacks[func_string] = func
        else:
            func_string = func

        def callback_wrapper(ch, method, properties, body):
            LOGGER.info("Got message - %s" % (method.routing_key))
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
            q_st = DEFAULT_QUEUE_SETTINGS.copy()
            q_st.update(q_settings)
            queue_name = q_name
            if queue_name.startswith("AUTO-"):
                queue_name = ""
            mthd_frame = channel.queue_declare(queue=queue_name, durable=q_st['DURABLE'],
                                               auto_delete=q_st['AUTO_DELETE'])
            queue_name = mthd_frame.method.queue
            LOGGER.debug('Declaring queue - %s' % queue_name)
            for binding in q_st['BINDINGS']:
                LOGGER.info("Binding the queue - %s with key %s" % (queue_name, binding))
                channel.queue_bind(exchange=self.settings.EXCHANGE, queue=queue_name,
                                   routing_key=binding)
            LOGGER.debug("Setting Basic consume for callback - %s " % q_st['CALLBACK'])
            channel.basic_consume(self.callback(q_st['CALLBACK']), queue=queue_name,
                                  no_ack=q_st['NO_ACK'], exclusive=q_st['EXCLUSIVE'])
