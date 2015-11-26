import json

from django.db.models.signals import post_save, post_delete
from django.core import serializers
from .settings import project_name, MODEL_DEFAULTS
from hedwig.core.settings import Settings
from .emitter import hedwig_emitter
import inspect

import logging

LOGGER = logging.getLogger(__name__)


def coerce_model_settings(instance):
    model_hedwig_dict = {}
    model_hedwig = getattr(instance, 'Hedwig', None)
    if inspect.isclass(model_hedwig):
        model_hedwig_dict = dict((name, getattr(model_hedwig, name)) for name in dir(model_hedwig) if not name.startswith('__'))
    return Settings(user_settings=model_hedwig_dict, defaults=MODEL_DEFAULTS)


def saved_hedwig_models(sender, instance, created, **kwargs):
    if created:
        action = 'created'
    else:
        action = 'updated'
    emit_hedwig_model_data(instance, action)


def deleted_hedwig_models(sender, instance, **kwargs):
    emit_hedwig_model_data(instance, 'deleted')


def emit_hedwig_model_data(instance, action):
    model_settings = coerce_model_settings(instance)
    if not getattr(model_settings, action, True):
        return True

    routing_key = '.'.join([project_name, instance._meta.app_label, 'model', instance._meta.object_name, action,
                            str(instance.pk)])
    show_fields = True
    serializer_kwargs = {}
    if isinstance(model_settings.fields, bool):
        show_fields = model_settings.fields
    else:
        serializer_kwargs['fields'] = model_settings.fields
    hedwig_json_obj = {}
    if show_fields:
        serializer_kwargs['use_natural_primary_keys'] = model_settings.natural_primary_keys
        serializer_kwargs['use_natural_foreign_keys'] = model_settings.natural_foreign_keys
        serializer_kwargs['format'] = "json"
        serializer_kwargs['queryset'] = [instance]
        try:
            hedwig_json_obj = json.loads(serializers.serialize(**serializer_kwargs))[0]
        except Exception as e:

            hedwig_json_obj = {'error': str(e)}

    payload = json.dumps(hedwig_json_obj)

    hedwig_emitter.emit(routing_key, payload)


def register_hedwig_callbacks():
    LOGGER.info("Registering post_save and post_delete signal callbacks")
    post_save.connect(saved_hedwig_models, weak=False, dispatch_uid="saved_hedwig_models")
    post_delete.connect(deleted_hedwig_models, weak=False, dispatch_uid="deleted_hedwig_models")
