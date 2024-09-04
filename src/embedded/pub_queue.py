import pika
import base64
import os

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

queue_name = 'image_queue'
image_path = 'image.jpg'  # Caminho da imagem já salva

# Conexão ao RabbitMQ
connection = get_connection()
channel = connection.channel()
channel.queue_declare(queue=queue_name, durable=True)

# Função para ler a imagem armazenada localmente e enviá-la para a fila RabbitMQ
def send_image_to_queue():
    try:
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')

            channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=image_base64,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Torna a mensagem persistente
                )
            )
            print("Imagem enviada para a fila")
    except Exception as e:
        print(f"Erro ao enviar a imagem para a fila: {e}")

if __name__ == '__main__':
    try:
        send_image_to_queue()
    except KeyboardInterrupt:
        print("Envio interrompido")
    finally:
        connection.close()
