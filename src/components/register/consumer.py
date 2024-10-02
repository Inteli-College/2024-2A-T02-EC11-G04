import pika
import sys
import base64
import boto3
import io
from PIL import Image
import json
import logging
import os

from client import PikaClient
from utils import Logger

_logger = Logger(__name__)._get_logger()

# Função para decodificar e enviar imagem para o S3
def decode_and_upload(base64_image: str, bucket_name: str, s3_file_name: str):
    try:
        # Decodificando a imagem base64
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))
        
        # Salvando a imagem como PNG em um objeto BytesIO
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        buffered.seek(0)  # Garantir que o ponteiro está no início do arquivo

        session = boto3.Session()
        credentials = session.get_credentials()
        _logger.info(session)

        # Ativa o log detalhado para o boto3
        boto3.set_stream_logger(name='boto3', level=logging.DEBUG)

        # Criando um cliente S3
        s3_client = boto3.client('s3')

        # Enviando a imagem para o S3
        s3_client.upload_fileobj(
            buffered,  # Arquivo a ser enviado
            bucket_name,  # Nome do bucket
            s3_file_name,  # Nome do arquivo no S3
            ExtraArgs={'ContentType': 'image/png'}  # Especifica o tipo de conteúdo
        )

        _logger.info(f"Imagem {s3_file_name} enviada com sucesso para o bucket {bucket_name}")

    except Exception as e:
        _logger.error(f"Ocorreu um erro ao enviar a imagem para o S3: {str(e)}")

class PikaConsumer(PikaClient):
    def __init__(self):
        super().__init__()
        self._channel = self.connect_to_broker()

    def on_message_received(self, channel, method, properties, body) -> None:
        try:
            # Assumindo que a mensagem recebida é uma string base64 de uma imagem
            message = json.loads(body.decode('utf-8'))
            _logger.info(message)


            bucket_name = 'bucket-greench'  # Defina o nome do bucket S3
            s3_file_name = message["image_metadata"]["image_name"] # Defina o nome do arquivo no S3
            _logger.info(s3_file_name)
            # Enviando a imagem para o S3
            decode_and_upload(message["image"], bucket_name, s3_file_name)
            # Acknowledge a mensagem
            # channel.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            _logger.error(f"Erro ao processar a mensagem: {str(e)}")
            # Em caso de erro, pode-se rejeitar a mensagem, se necessário
            channel.basic_nack(delivery_tag=method.delivery_tag)

    def start_consumer(self):
        self._channel.basic_consume(
            queue=self._amqp_routing_key,
            on_message_callback=self.on_message_received,
            auto_ack=True
        )
        _logger.info("Iniciando o consumidor RabbitMQ...")
        self._channel.start_consuming()

def main():
    pika_consumer = PikaConsumer()
    pika_consumer.start_consumer()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        _logger.info("Encerrando o consumidor RabbitMQ...")
        sys.exit(0)
