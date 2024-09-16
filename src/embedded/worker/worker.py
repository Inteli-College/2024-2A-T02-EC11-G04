import os
from queue import Empty
import threading


from messaging import PikaPublisher
from utils import Logger, DirectoryMonitor, ImageHandler

_logger = Logger(logger_name=__name__)._get_logger()

class Worker:
    def __init__(self, directory_monitor: DirectoryMonitor,
                image_compressor: ImageHandler) -> None:
        self._directory_monitor = directory_monitor
        self._image_compressor = image_compressor
        self._publisher = PikaPublisher()
        self._stop_flag = threading.Event()

    def run(self):
        """Start the worker process to continuously monitor the directory and process images."""
        self._directory_monitor.start_monitoring()
        while not self._stop_flag.is_set():
            _logger.debug("Worker running...")
            try:
                image_path = self._directory_monitor._local_bus.get(timeout=5)
                processed_image = self._image_compressor.process_image(image_path)
                self._publisher.publish_message(processed_image)
                _logger.info(f"Compressed image: {image_path}")
                self._directory_monitor._local_bus.task_done()
                os.remove(image_path)
                _logger.info("Image processed and removed both directory and bus: %s", 
                            image_path)
            except Empty:
                _logger.info("No new images to process. Waiting for new images.")
                continue

    def stop(self):
        """Stops the worker gracefully."""
        self._stop_flag.set()

    def start_thread(self):
        """Start worker in a separate thread."""
        worker_thread = threading.Thread(target=self.run)
        worker_thread.daemon = True
        worker_thread.start()
