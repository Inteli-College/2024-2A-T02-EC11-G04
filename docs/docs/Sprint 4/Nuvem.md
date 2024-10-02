---
title: Nuvem
sidebar_position: 1
---

# Processamento e armazenamento de imagens em nuvem

## Introdução

Esta seção descreve o funcionamento de um serviço responsável por consumir mensagens de uma fila RabbitMQ e enviar imagens para o Amazon S3, um sistema de armazenamento de arquivos da AWS. Este serviço está inserido em um pipeline de processamento de imagens, onde o objetivo é realizar a segmentação semântica de áreas florestais em um ambiente embarcado e, posteriormente, utilizar um modelo de visão computacional na nuvem para realizar a contagem de árvores.

No contexto deste projeto, as imagens são inicialmente processadas em um dispositivo embarcado para identificar regiões florestais de interesse. Essas imagens são então enviadas para um servidor EC2 na nuvem, que consome as imagens a partir de uma fila RabbitMQ, as processa e as armazena no Amazon S3, onde ficam disponíveis para outras etapas do pipeline, como a contagem de árvores usando algoritmos de visão computacional.

### Objetivo

O objetivo deste serviço é:

1. Consumir mensagens contendo imagens codificadas em Base64 a partir de uma fila RabbitMQ.
2. Decodificar as imagens e enviá-las para um bucket do Amazon S3.
3. Garantir que as imagens estejam disponíveis no S3 para processamento posterior.

## Funcionamento do Código

O código discutido acima é dividido em dois componentes principais: o Consumer RabbitMQ e o Upload para o S3.

#### 1. RabbitMQ Consumer

O código implementa um consumidor de mensagens da fila RabbitMQ, utilizando a biblioteca `pika` para gerenciar a conexão com o broker e consumir as mensagens enviadas ao servidor EC2.

- A classe `PikaConsumer` herda de uma classe base `PikaClient` e se conecta ao RabbitMQ para consumir mensagens de uma fila.
- O método `on_message_received` é responsável por processar cada mensagem recebida. A mensagem é esperada em formato JSON e contém a imagem codificada em Base64 e seus metadados (como o nome do arquivo).
- A função `basic_ack` garante que, após o processamento bem-sucedido de cada mensagem, o RabbitMQ a remova da fila.

#### 2. Decodificação e Upload para o S3

A função `decode_and_upload` é responsável por:

- Decodificar a imagem que está em formato Base64.
- Armazenar a imagem em um buffer de memória temporário no formato PNG.
- Enviar a imagem para um bucket do S3 utilizando o cliente `boto3`.

O código utiliza a função `boto3.Session()` para criar uma sessão AWS e autenticar o envio da imagem para o S3. Ele também verifica se as credenciais da AWS estão disponíveis e corretamente configuradas no ambiente da instância EC2. As imagens são enviadas para o bucket configurado com um nome de arquivo específico, extraído dos metadados da imagem.

### Estrutura do código

#### 1. Conexão com RabbitMQ:

```
class PikaConsumer(PikaClient):
    def start_consumer(self):
        self._channel.basic_consume(
            queue=self._amqp_routing_key,
            on_message_callback=self.on_message_received,
            auto_ack=True
        )
        self._channel.start_consuming()
```

#### 2. Processamento e Upload para o S3:

```
def decode_and_upload(base64_image: str, bucket_name: str, s3_file_name: str):
    image_data = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_data))
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    buffered.seek(0)
    
    session = boto3.Session()
    s3_client = boto3.resource('s3')
    s3_client.Bucket(bucket_name).upload_fileobj(buffered, s3_file_name)
```
#### 3. Recepção de Mensagem e Decodificação:

```
def on_message_received(self, channel, method, properties, body):
    message = json.loads(body.decode('utf-8'))
    decode_and_upload(message["image"], "bucket-greench", message["image_metadata"]["image_name"])
```
## Conclusão

Este serviço é uma parte essencial de um pipeline de processamento de imagens para a contagem de árvores em regiões florestais. Ele integra uma solução baseada em nuvem com um sistema embarcado, onde imagens capturadas e processadas localmente são enviadas para a nuvem para processamento adicional. O código utiliza o RabbitMQ para garantir o fluxo assíncrono das imagens entre o dispositivo embarcado e a nuvem, enquanto o Amazon S3 oferece uma solução escalável e eficiente para o armazenamento das imagens.

Ao garantir a correta recepção e armazenamento das imagens no S3, este sistema viabiliza o uso posterior de algoritmos avançados de visão computacional para contagem de árvores, permitindo a automação e monitoramento eficaz de áreas florestais. Além disso, o uso de práticas como logging detalhado e a utilização da sessão AWS permite o diagnóstico e resolução rápida de erros relacionados à falta de credenciais ou falhas de conexão.