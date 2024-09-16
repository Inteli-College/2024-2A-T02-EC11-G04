
import sys
from queue import Queue
from utils import DirectoryMonitor, ImageHandler, Logger
from worker import Worker

_logger = Logger(logger_name=__name__)._get_logger()

workers = []

def main():
    image_queue = Queue()

    directory_monitor = DirectoryMonitor(directory="images", local_bus=image_queue)

    image_handler = ImageHandler()

    num_workers = 2

    for _ in range(num_workers):
        worker = Worker(directory_monitor=directory_monitor, image_compressor=image_handler)
        workers.append(worker)
        worker.start_thread()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        _logger.info("Shutting down workers...")
        for worker in workers:
            worker.stop()
        sys.exit(0)

if __name__ == "__main__":
    main()
