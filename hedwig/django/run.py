__author__ = 'sandeep'
import sys

from hedwig.core.service import ServiceManager
from hedwig.core.worker import HedwigWorker
import django

django.setup()
from .settings import hedwig_settings


def main(argv):
    msg_service = ServiceManager(HedwigWorker, num_workers=2)
    msg_service.start(settings=hedwig_settings)


if __name__ == "__main__":
    main(sys.argv[1:])
