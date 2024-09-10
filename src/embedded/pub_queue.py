import cv2
import numpy as np
import json
import pika
import os
import time
import base64
import uuid

# Função para processar e extrair metadados de uma imagem
def process_image(image_path):
    # Carrega a imagem em escala de cinza
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Encontra os contornos na imagem
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calcula a área do maior contorno encontrado
    if contours:
        area = cv2.contourArea(contours[0])
    else:
        area = 0

    # Gera um GUID para identificar a imagem
    image_guid = str(uuid.uuid4())

    # Lê a imagem original em formato binário e a converte para base64
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    # Metadados que serão enviados
    metadata = {
        "image_metadata": {
            "guid": image_guid,
            "image_name": os.path.basename(image_path),
            "area": area
        }
    }

    return image_base64, metadata

# Função para configurar a conexão com RabbitMQ
def get_connection():
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "10.128.0.44")
    rabbitmq_port = int(os.getenv("RABBITMQ_PORT", 5672))
    rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER", "grupo4")
    rabbitmq_pass = os.getenv("RABBITMQ_DEFAULT_PASS", "grupo4")

    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
    parameters = pika.ConnectionParameters(
        host=rabbitmq_host, port=rabbitmq_port, credentials=credentials
    )

    connection = pika.BlockingConnection(parameters)
    return connection

# Função para publicar a mensagem na fila
def publish_message(connection, queue_name, message):
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message)
    
    print(f"Mensagem enviada para a fila '{queue_name}'.")

# Função para monitorar o diretório, processar as imagens e enviá-las para a fila
def monitor_directory(directory, image_queue_name, data_queue_name):
    # Conexão ao RabbitMQ
    connection = get_connection()

    while True:
        # Lista todos os arquivos no diretório
        files = os.listdir(directory)

        for file_name in files:
            # Ignora arquivos ocultos e que não sejam imagens PNG
            if not file_name.startswith('.') and file_name.endswith('.png'):
                file_path = os.path.join(directory, file_name)

                # Processa a imagem e extrai a imagem em base64 e os metadados
                image_base64, metadata = process_image(file_path)

                # Serializa a imagem em base64 para JSON
                image_message = json.dumps({
                    "guid": metadata["image_metadata"]["guid"],
                    "image": image_base64
                })

                # Serializa os metadados para JSON
                metadata_message = json.dumps(metadata)

                # Envia a imagem para a fila 'queue_image_queue'
                publish_message(connection, image_queue_name, image_message)

                # Envia os metadados para a fila 'data_queue'
                publish_message(connection, data_queue_name, metadata_message)

                # Remove a imagem do diretório após o envio
                os.remove(file_path)
                print(f"Imagem '{file_name}' processada, enviada e excluída.")

        # Aguardar 5 segundos antes de verificar novamente (pode ajustar o intervalo conforme necessário)
        time.sleep(5)

    connection.close()

# Diretório onde as imagens serão salvas
directory_to_watch = 'captures'

# Nomes das filas no RabbitMQ
image_queue_name = 'queue_image_queue'
data_queue_name = 'data_queue'

# Inicia o monitoramento do diretório
monitor_directory(directory_to_watch, image_queue_name, data_queue_name)
