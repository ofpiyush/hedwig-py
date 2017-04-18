import logging

from importlib import import_module

LOGGER = logging.getLogger(__name__)


def import_obj(cb):
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
