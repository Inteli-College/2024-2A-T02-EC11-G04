import sys
from queue import Queue
import threading
from fastapi import FastAPI, HTTPException
import uvicorn

from messaging import PikaPublisher
from utils import DirectoryMonitor, ImageHandler, Logger, CaptureHandler
from worker import Worker

_logger = Logger(logger_name=__name__)._get_logger()

app = FastAPI()  # Inicializa o FastAPI

# Defina os diretórios para as imagens
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_IMAGES_DIR = os.getenv('INPUT_DIRECTORY', 'test_images')

capture_handler = CaptureHandler()
image_handler = ImageHandler(model_name="model_segformer")

def find_image_with_possible_extensions(image_name):
    """
    Tenta encontrar a imagem com extensões .png, .jpeg ou .jpg
    """
    possible_extensions = ['.png', '.jpeg', '.jpg']
    for ext in possible_extensions:
        image_path_with_ext = os.path.join(TEST_IMAGES_DIR, image_name + ext)
        if os.path.exists(image_path_with_ext):
            return image_path_with_ext
    return None

# Rotas da API
@app.get("/capture-and-process")
def capture_and_process_image():
    """
    Captura e processa uma imagem, disparando o fluxo no worker.
    """
    capture_handler.capture_image()
    return {"status": "Worker triggered for image capture and processing"}

@app.get("/process-image/{image_name}")
def process_image(image_name: str):
    """
    Processa a imagem, adicionando automaticamente uma extensão se necessário.
    """
    # Tenta encontrar a imagem com as possíveis extensões
    image_path = find_image_with_possible_extensions(image_name)

    print("Image path:", image_path)

    if not image_path:
        raise HTTPException(status_code=404, detail=f"Image {image_name} not found with .png, .jpeg, or .jpg extensions.")

    image_handler.process_image(image_path)
    return {"status": f"Worker triggered for processing the image {os.path.basename(image_path)}"}

def main():
    image_queue = Queue()
    
    # Inicia o monitoramento do diretório
    directory_monitor = DirectoryMonitor(directory="images", local_bus=image_queue)
    
    # Inicializa os outros componentes
    image_handler = ImageHandler(model_name="model_segformer")
    pika_publisher = PikaPublisher()
    
    worker = Worker(directory_monitor=directory_monitor, 
                    image_handler=image_handler,
                    pika_publisher=pika_publisher)
    
    # Inicia o worker em uma thread separada
    worker.start_worker()
    
    # Inicia o servidor FastAPI em uma thread separada
#    uvicorn.run(app, host="0.0.0.0", port=8000)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        _logger.info("Shutting down workers...")
        worker.stop_worker()
        sys.exit(0)

if __name__ == "__main__":
    main()
