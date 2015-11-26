from rest_framework.serializers import ModelSerializer
from rest_framework.renderers import JSONRenderer
from hedwig.django.settings import project_name
from .settings import hedwig_rest_framework_settings
from hedwig.django.emitter import hedwig_emitter


class HedwigModelSerializer(ModelSerializer):
    def save(self, **kwargs):
        action = 'created'
        if self.instance is not None:
            action = 'updated'
        super(HedwigModelSerializer, self).save(**kwargs)
        emit_hedwig_serializer_data(action, self.__module__.split('.')[0], self.__class__.__name__, self)
        return self.instance


def emit_hedwig_serializer_data(action, module_name, serializer_name, serializer):
    if not bool(hedwig_rest_framework_settings.SERIALIZER_SIGNALS):
        return

    routing_key = '.'.join([project_name, module_name, 'serializer', serializer_name, action,
                            str(serializer.instance.pk)])
    json_renderer = JSONRenderer()
    hedwig_emitter.emit(routing_key, json_renderer.render(serializer.data))
