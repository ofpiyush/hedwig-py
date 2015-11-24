from importlib import import_module
import logging
from hedwig.core.base import Base


class Consumer(Base):
    def consume(self):
        logging.debug('Hedwig: Consumer Initialized')
        self.connect()
        channel = self.create_channel()
        self._bind_things(channel)

        try:
            logging.info('Hedwig: Start consuming')
            channel.start_consuming()
        except KeyboardInterrupt:
            self.close_channel(channel)
            self.shutdown()

        except Exception:
            self.close_channel(channel)
            self.shutdown()

    def callback(self, func):
        def callback_wrapper(ch, method, properties, body):
            try:
                func(ch, method, properties, body)
            except Exception as e:
                print e.message

        return callback_wrapper

    def _bind_things(self, channel):
        logging.debug('Hedwig: Attempting to bind queues')
        for q_name, q_settings in self.settings.CONSUMER['QUEUES'].iteritems():
            logging.debug('Hedwig: Declaring queue - {0}'.format(q_name))
            channel.queue_declare(queue=q_name, durable=q_settings['DURABLE'], auto_delete=q_settings['AUTO_DELETE'])
            for binding in q_settings['BINDINGS']:
                logging.info("Hedwig: Binding the queue - {0} with key {1}".format(q_name, binding))
                channel.queue_bind(exchange=self.settings.EXCHANGE, queue=q_name,
                                   routing_key=binding)
            logging.debug("Hedwig: Setting Basic consume for callback - {0}".format(q_settings['CALLBACK']))
            channel.basic_consume(self.callback(self._import(q_settings['CALLBACK'])), queue=q_name,
                                  no_ack=q_settings['NO_ACK'])

    def _import(self, cb):
        logging.debug("Hedwig: Attempting to import - {0}".format(cb))
        try:
            # Nod to DRF for nod to tastypie's use of importlib.
            parts = cb.split('.')
            module_path, callback_name = '.'.join(parts[:-1]), parts[-1]
            logging.debug("Hedwig: Importing {0} from {1}".format(callback_name, module_path))
            module = import_module(module_path)
            return getattr(module, callback_name)
        except (ImportError, AttributeError) as e:
            msg = "Could not import '%s' %s: %s." % (cb, e.__class__.__name__, e)
            raise ImportError(msg)
