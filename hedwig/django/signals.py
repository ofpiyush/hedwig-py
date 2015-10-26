from django.db.models.signals import post_save, post_delete
from django.db.models.fields.related import ManyToManyField
import json
from .settings import project_name


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
        else:
            data[f.name] = f.value_from_object(instance)

    return data


def saved_hedwig_models(sender, instance, created, **kwargs):
    if created:
        action = 'created'
    else:
        action = 'updated'
    emit_hedwig_model_data(instance, action)


def deleted_hedwig_models(sender, instance, **kwargs):
    emit_hedwig_model_data(instance, 'deleted')


def emit_hedwig_model_data(instance, action):
    try:
        hide_fields = bool(instance.Hedwig.hide_fields)
    except AttributeError:
        hide_fields = True

    routing_key = '.'.join([project_name, instance._meta.app_label, 'model', instance._meta.object_name, action,
                            str(instance.pk)])
    if hide_fields:
        payload = {}
    else:
        payload = to_dict(instance)

    print routing_key, json.dumps(payload)


post_save.connect(saved_hedwig_models, weak=False, dispatch_uid="saved_hedwig_models")
post_delete.connect(deleted_hedwig_models, weak=False, dispatch_uid="deleted_hedwig_models")
