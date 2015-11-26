__author__ = 'sandeep'
import signal
import time
import sys

import multiprocessing
import inspect
import traceback
import logging


LOGGER = logging.getLogger(__name__)


class ServiceManager(object):
    def __init__(self, worker_cls, num_workers=2):
        if not (inspect.isclass(worker_cls) and issubclass(worker_cls, multiprocessing.Process)):
            raise ValueError("Worker class must extend multiprocessing.Process")
        self.workers = []
        self.num_workers = num_workers
        self.worker_cls = worker_cls
        self.running = False
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def start(self, *args, **kwargs):
        self.running = True
        LOGGER.info("Starting: Hedwig Worker Service...")
        try:
            while self.running:
                if len(self.workers) < self.num_workers:
                    worker = self.worker_cls(*args, **kwargs)
                    worker.start()
                    self.workers.append(worker)
                else:
                    for worker in self.workers:
                        if not worker.is_alive():
                            worker.shutdown()
                            self.workers.remove(worker)
                            worker.terminate()
                    time.sleep(5)

        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            LOGGER.exception(str(e))
            traceback.print_exc(file=sys.stdout)
            self.stop()

    def stop(self, signum=None, frame=None):
        self.running = False
        LOGGER.info("Stopping: Hedwig Worker Service...")
        for worker in self.workers:
            LOGGER.info("Stopping Worker: " + worker.name)
            worker.shutdown()
            worker.terminate()
        sys.exit(0)

    def is_running(self):
        return self.running
