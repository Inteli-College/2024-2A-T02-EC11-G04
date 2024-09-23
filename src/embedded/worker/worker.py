import os
from queue import Empty
import threading

from messaging import PikaPublisher
from utils import DirectoryMonitor, ImageHandler, Logger 

_logger = Logger(logger_name=__name__)._get_logger()


class Worker:
    def __init__(self, directory_monitor: DirectoryMonitor,
                image_handler: ImageHandler,
                pika_publisher: PikaPublisher) -> None:
        self._directory_monitor = directory_monitor
        self._image_handler = image_handler
        self._publisher = pika_publisher
        self._stop_flag = threading.Event()

    def run(self):
        """Start the worker process to continuously monitor the directory and process images."""
        self._directory_monitor.start_monitoring()
        while not self._stop_flag.is_set():
            try:
                image_path = self._directory_monitor._local_bus.get()
                _logger.info("Processing image: %s", image_path)
                processed_image = self._image_handler.process_image(image_path)
                _logger.info("Image processed: %s", image_path)
                self._publisher.publish_message(processed_image)
                _logger.info("Image published: %s", image_path)
                self._directory_monitor._local_bus.task_done()
                os.remove(image_path)
                _logger.info("Image processed and removed from both directory and bus: %s", 
                            image_path)
            except Empty:
                continue

    def start_worker(self):
        """Start worker in a separate thread."""
        worker_thread = threading.Thread(target=self.run, daemon=True)
        worker_thread.start()
        _logger.info("Worker initialized")

    def stop_worker(self):
        """Stops the worker gracefully."""
        self._stop_flag.set()
        self._directory_monitor.stop_monitoring()
        _logger.info("Worker stopped.")
