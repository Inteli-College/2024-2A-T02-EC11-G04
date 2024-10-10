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
from uuid import uuid4, UUID
from sqlalchemy.types import String, Float


from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import insert

DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@prod-db.c8q700syfk11.us-east-1.rds.amazonaws.com:5432/postgres"
engine = create_engine(DATABASE_URL)
session_db = Session(bind=engine)

Base = declarative_base()

_logger = Logger(__name__)._get_logger()

class ImageMetadata(Base):
    __tablename__ = 'image_metadata'

    id = Column(String, primary_key=True, autoincrement=False)
    image_name = Column(String, nullable=False)
    mask_area_pixels = Column(Integer, nullable=False)
    mask_percentage = Column(Float, nullable=False)

# Função para criar a tabela
def create_table(engine):
    Base.metadata.create_all(engine)

create_table(engine)
_logger = Logger(__name__)._get_logger()

# Função para decodificar e enviar imagem para o S3
def decode_and_upload(base64_image: str, bucket_name: str, s3_file_name: str):
    try:
        # Decodificando a imagem base64
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))
        
        # Salvando a imagem como PNG em um objeto BytesIO
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        buffered.seek(0)  # Garantir que o ponteiro está no início do arquivo

#        session = boto3.Session(
#        aws_access_key_id='ASIA3NDYPRREVYCDMHAH',
#        aws_secret_access_key='/Zv2jV2/RDCgoBjHrUMQgW08vVHvdktUBz/EZihR',
#        aws_session_token='IQoJb3JpZ2luX2VjEM3//////////wEaCXVzLXdlc3QtMiJHMEUCIQCAtLAMNPK7OKfZ6Xmu3vFsczi+VUZYWxkcolUp8aAdEgIgJfIA61b8tl+IIYqP5jfFDjxkXm5XKBsWPDKAKokop3EqqQIIFhABGgw3ODQwODQyMDg3MTMiDHGQUFUtwrAAPnlWFyqGAtuIz0w6d+NQq5HK7ytcaOzi2NirCMsDAHHZOPBhaXFxtryEX9HGLdsJjlJprlqhohdW6cSccJ3zIcwE6KINleBf+sRl1F1tDAGPLxiCxd7iqZIUYUtdlls59BD9K13kU0X0lqqs1tScdYBT4B6fd99lpAAE7zh1sYkmyenH0OtIuPKvI6W52ApXgVX2pOPExH+XoNc2I02sg37kQOY7x1dP9XAuke1m9Aj29eNBCYquW4O35A/Nq3xHc4oBFuc2lYhjnwd+9hpxNtllpklPx7sX9sI9M1TVs+N8T4T9O4eKW8xu5J0gq37lZ+mK9+dfNfZoQriMtDP6qoc5Wk8UzUWhVaUovIUwsaTVtwY6nQFQ1M+WwUujNNAtZDcoKSmRhUthKHj0S9TUSUDeNlQ7uAE0RdUn5OJc0O5FSTbMmAzEkKr7b/bQM3HfFVf8qPlUIEi3sxpYT3502JOyKjO/u5JxD+aaNKe6bMs2SX6kw9R8m2J4sd5pQLO11nVztw6HRpAi0o3qapmCHDcQA43Cv3hRMuNwt0kk3c/uq49+vi2x2qiFmgbfq6VsDpQl')
        #credentials = session.get_credentials()
#        _logger.info(session)

        # Ativa o log detalhado para o boto3
        boto3.set_stream_logger(name='boto3', level=logging.DEBUG)

        # Criando um cliente S3
        s3_client = boto3.client('s3',
        aws_access_key_id='ASIAXDLA5ISI5HDVKCGG',
        aws_secret_access_key='RXaBukJN+otjDZtTFL1wSEshLRKMk5wfdMeG3Z/H',
        aws_session_token='IQoJb3JpZ2luX2VjEBUaCXVzLXdlc3QtMiJHMEUCIE/IdHS1NnfK1V4kCV8gaosYSwkpqneLSF0tbXll4HUcAiEAxtSkf2e5KdGC/rc1ZNQtcxz5JjWfnuHr41QwXzd+dPsqpAIIbhAAGgw0ODgyMTg5MDM2OTciDIGwOU+wXEnsuhYL9SqBAjNLYzLFZ7Mp+SrVQC/xzo9YJCzHNCuVjuVlrK+GHNv1dbOLt2rWMmZXV+vlu2eCn4WpH0gPiHu7Jzo3wTGXhw1BRqpqeX/I7NPaSWnb7OMJEQA7ZaNKcxE57OMNsaXkxR3ujLptgi4a5qVkY7lvWRg9IobnPoc5Uz9e5HUbIdU4m+U7fMMwN1fvLDneKain5gDmEoBTnAU7YFoFJoz72pznO9jTbqb7B4YGhP72w/QaF8gqn4X7YEZL0FUy+4ZEZYrSLdP221ITvb68jma5511k7BKbeWTrW06tMrKssrleIWBErzUK5tcxK7W0shSsDBhaBgSzrVlR1XkhH5XyGc5MMLS4nbgGOp0BeH8e0iWORhrgAtqbgz3SZI/k0o47e6/48ZzUlNE3CdKB/uptAXrHQccDA34SHj94pzRHf5I3X0vkAFcMQ13LINcmlTCHbakYjH3S1a2k5AJh4x/QBq27pqYS4hYm9W00A7Uvce0+CW3XIi2lX+WTpfDTh0ONdBMt1twkXnfq3/lucXbjt+gq7A+KjwcWG5CCFxI1yVhK/m6jvbT4TA==')
        _logger.info("Client stablished")
        # Enviando a imagem para o S3
        s3_client.upload_fileobj(
            buffered,  # Arquivo a ser enviado
            bucket_name,  # Nome do bucket
            s3_file_name,  # Nome do arquivo no S3
            ExtraArgs={'ContentType': 'image/jpeg'}  # Especifica o tipo de conteúdo
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


            bucket_name = 'bucket-greentch'  # Defina o nome do bucket S3
            s3_file_name = message["image_name"] # Defina o nome do arquivo no S3
            _logger.info(s3_file_name)
            # Enviando a imagem para o S3
            image_name = message["image_name"]
            mask_area_pixels = message["mask_area_pixels"]
            mask_percentage = message["mask_percentage"]
            connection = engine.connect()

            query = insert(ImageMetadata).values(
            id=str(uuid4()),
            image_name=message["image_name"],
            mask_area_pixels=message["mask_area_pixels"],
            mask_percentage=message["mask_percentage"]
            )
            connection.execute(query)
            connection.commit()
            decode_and_upload(message["image_base64"], bucket_name, s3_file_name)
            # Acknowledge a mensagem
            channel.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            _logger.error(f"Erro ao processar a mensagem: {str(e)}")
            # Em caso de erro, pode-se rejeitar a mensagem, se necessário
            channel.basic_nack(delivery_tag=method.delivery_tag)

    def start_consumer(self):
        self._channel.basic_consume(
            queue=self._amqp_routing_key,
            on_message_callback=self.on_message_received,
            auto_ack=False
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
