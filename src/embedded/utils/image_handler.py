import base64
import json

from .logger import Logger

_logger=Logger(logger_name=__name__)._get_logger()


class ImageHandler:
    """Class for image compression"""

    def __init__(self) -> None:
        _logger.info("Image handler initialized.")

    @staticmethod
    def process_image(file_path) -> str:
        """Process the image and extract the image in base64 format.

        Args:
            file_path (str): Path to the image file.

        Returns:
            base64: Compressed image in base64 format. 
        """
        with open(file_path, "rb") as image_file:
            image = image_file.read()
            image_base64 = base64.b64encode(image).decode("utf-8")
            metadata = {
                "image": image_base64, 
                "image_metadata": { 
                    "image_name": "teste", 
                    "area": 0 #TODO: Implement area calculation @jeanroths/@joaocarazzato
                    } 
                }
        return json.dumps(metadata)
