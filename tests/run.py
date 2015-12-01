from hedwig.core.service import ServiceManager
from hedwig.core.worker import HedwigWorker
from .settings import hedwig_settings
import sys


def main(argv):
    msg_service = ServiceManager(HedwigWorker, num_workers=1)
    msg_service.start(settings=hedwig_settings)


if __name__ == "__main__":
    main(sys.argv[1:])
