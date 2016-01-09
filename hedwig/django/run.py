__author__ = 'sandeep'
import sys

from hedwig.core.service import ServiceManager
from .worker import DjangoHedwigWorker


def main(argv):
    msg_service = ServiceManager(DjangoHedwigWorker, num_workers=2)
    msg_service.start()


if __name__ == "__main__":
    main(sys.argv[1:])
