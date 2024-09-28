import os
from pathlib import Path
from queue import Queue
import time
import threading

from .logger import Logger

_logger = Logger(logger_name=__name__)._get_logger()

class DirectoryMonitor:
    """Monitors a directory continuously for image files and places them in a processing queue."""
    
    def __init__(self, directory: str, local_bus: Queue, poll_interval: float = 60.0) -> None:
        """Initialize the directory monitor.
        
        Args:
            directory (str): Path to the directory to monitor.
            local_bus (Queue): A queue to hold image paths for processing.
            poll_interval (int): Time interval (in seconds) between directory checks.
        """
        self._directory = Path(directory)
        self._local_bus = local_bus
        self._poll_interval = poll_interval
        self._stop_polling = threading.Event()

    def processing_images_bus(self) -> None:
        """Continuously monitor the directory for new image files and place them in the queue."""
        processed_files = set()
        
        while not self._stop_polling.is_set():
            try:
                if not self._directory.exists():
                    os.mkdir(self._directory)
                
                for image_path in self._directory.iterdir():
                    if image_path.is_file() and not image_path.name.startswith('.') and image_path.suffix.lower() == '.png' or '.jpg':
                        if image_path not in processed_files:
                            self._local_bus.put(image_path)
                            processed_files.add(image_path)
                            _logger.info("Image added to the processing bus: %s", image_path)

                _logger.info("Files processed: %s", processed_files)
                time.sleep(self._poll_interval)
                _logger.info("Directory pooled for new images.")
                processed_files.clear()

            except Exception as e:
                _logger.error(f"Error during directory monitoring: {str(e)}")
                time.sleep(self._poll_interval)

    def start_monitoring(self) -> None:
        """Start the directory monitoring in a background thread."""
        monitor_thread = threading.Thread(target=self.processing_images_bus, daemon=True)
        monitor_thread.start()
        _logger.info("Directory monitoring initialized for directory: %s", self._directory)

    def stop_monitoring(self) -> None:
        """Stop the directory monitoring loop."""
        self._stop_polling.set()
        _logger.info("Directory monitoring stopped")
