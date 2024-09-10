import cv2
import json
import pika
import os
import base64
import uuid

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

# Função para salvar a imagem decodificada no diretório especificado
def save_image(image_guid, image_data):
    image_directory = 'processed_images'
    os.makedirs(image_directory, exist_ok=True)
    
    image_path = os.path.join(image_directory, f"{image_guid}.png")
    with open(image_path, "wb") as image_file:
        image_file.write(base64.b64decode(image_data))
    
    print(f"Imagem salva como {image_path}")

# Função para processar as mensagens da fila de imagens
def process_image_queue(ch, method, properties, body):
    # Deserializa o JSON recebido
    message = json.loads(body)
    image_guid = message['guid']
    image_data = message['image']

    # Salva a imagem no diretório
    save_image(image_guid, image_data)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Imagem com GUID {image_guid} processada e salva.")

# Função para processar as mensagens da fila de metadados
def process_data_queue(ch, method, properties, body):
    # Deserializa o JSON recebido
    metadata = json.loads(body)
    
    image_guid = metadata['guid']
    image_metadata = metadata['image_metadata']

    # Exibe ou salva os metadados conforme necessário
    print(f"Metadados recebidos para a imagem {image_guid}: {image_metadata}")

    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Metadados para a imagem com GUID {image_guid} processados.")

# Função principal para consumir as mensagens das filas
def consume_queues():
    connection = get_connection()
    channel = connection.channel()

    # Consome mensagens da fila de imagens
    channel.queue_declare(queue='queue_image_queue', durable=True)
    channel.basic_consume(queue='queue_image_queue', on_message_callback=process_image_queue)

    # Consome mensagens da fila de metadados
    channel.queue_declare(queue='data_queue', durable=True)
    channel.basic_consume(queue='data_queue', on_message_callback=process_data_queue)

    print("Esperando mensagens. Pressione CTRL+C para sair.")
    channel.start_consuming()

# Inicia o consumo das filas
consume_queues()
