import sys
from queue import Queue

from messaging import PikaPublisher
from utils import DirectoryMonitor, ImageHandler, Logger
from worker import Worker

_logger = Logger(logger_name=__name__)._get_logger()

def main():
    image_queue = Queue()

    directory_monitor = DirectoryMonitor(directory="images", local_bus=image_queue)

    image_handler = ImageHandler()

    pika_publisher = PikaPublisher()

    worker = Worker(directory_monitor=directory_monitor, 
                    image_handler=image_handler,
                    pika_publisher=pika_publisher)
    worker.start_worker()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        _logger.info("Shutting down workers...")
        worker.stop_worker()
        sys.exit(0)

if __name__ == "__main__":
    main()
