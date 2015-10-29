__author__ = 'sandeep'
import sys
from hedwig.core.service import ServiceManager
from hedwig.core.worker import HedwigWorker
from django.conf import settings
import django


def main(argv):
    django.setup()
    USER_SETTINGS = getattr(settings, 'HEDWIG', None)
    msg_service = ServiceManager(HedwigWorker(settings=USER_SETTINGS), num_workers=2)
    msg_service.start()

if __name__ == "__main__":
    main(sys.argv[1:])

