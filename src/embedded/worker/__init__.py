# Package metadata
__version__ = "1.0.0"
__author__ = "greentech"


# Packge modules, submodules and functions importing
from .worker import Worker
from utils import ImageHandler
from messaging import PikaPublisher

# Inicializando os handlers e o publisher
image_handler = ImageHandler(model_name="model_segformer")
pika_publisher = PikaPublisher()

# Inicialize o worker_instance passando as instâncias dos handlers e publisher
worker_instance = Worker(
    directory_monitor=None,  # Ou passe a instância correta de DirectoryMonitor
    image_handler=image_handler,
    pika_publisher=pika_publisher
)

# Defined importing for '*' wildcard
__all__ = ["Worker"]
