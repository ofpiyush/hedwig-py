from importlib import import_module

from hedwig.core.base import Base


class Consumer(Base):

    def consume(self):
        self.connect()
        channel = self.create_channel()
        self._bind_things(channel)

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            self.close_channel(channel)
            self.shutdown()

        except Exception:
            self.close_channel(channel)
            self.shutdown()

    def callback(self, ch, method, properties, body):
        pass

    def _bind_things(self, channel):
        for q_name, q_settings in self.settings.CONSUMER['QUEUES'].iteritems():
            channel.queue_declare(queue=q_name, durable=q_settings['DURABLE'])
            for binding in q_settings['BINDINGS']:
                channel.queue_bind(exchange=self.settings.EXCHANGE, queue=q_name,
                                   routing_key=binding)
            channel.basic_consume(self._import(q_settings['CALLBACK']), queue=q_name)

    def _import(self, cb):
        try:
            # Nod to DRF for nod to tastypie's use of importlib.
            parts = cb.split('.')
            module_path, callback_name = '.'.join(parts[:-1]), parts[-1]
            module = import_module(module_path)
            return getattr(module, callback_name)
        except (ImportError, AttributeError) as e:
            msg = "Could not import '%s' %s: %s." % (cb, e.__class__.__name__, e)
            raise ImportError(msg)
