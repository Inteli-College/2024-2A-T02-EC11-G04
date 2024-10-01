---
title: Consumer  
sidebar_position: 3  
---

# Consumidor RabbitMQ

## Introdução

Esta seção descreve o funcionamento de um serviço responsável por consumir mensagens de uma fila RabbitMQ e enviar imagens para o Amazon S3, um sistema de armazenamento de arquivos da AWS. Este serviço faz parte de um pipeline de processamento de imagens, onde o objetivo principal é realizar a segmentação semântica de áreas florestais e, posteriormente, utilizar modelos de visão computacional para contagem de árvores.

No contexto deste projeto, as imagens são inicialmente processadas em um dispositivo embarcado para identificar regiões florestais de interesse. Essas imagens são enviadas para um servidor, que consome as imagens a partir de uma fila RabbitMQ, as processa e as armazena no Amazon S3, onde ficam disponíveis para outras etapas do pipeline, como a contagem de árvores usando algoritmos de visão computacional.

### Objetivo

O objetivo deste serviço é:

1. Consumir mensagens contendo imagens codificadas em Base64 de uma fila RabbitMQ.
2. Decodificar as imagens e enviá-las para um bucket no Amazon S3.
3. Garantir que as imagens estejam disponíveis no S3 para processamento posterior.

## Funcionamento do Código

O código é dividido em dois componentes principais: o **Consumer RabbitMQ** e o **Upload para o S3**.

### 1. RabbitMQ Consumer

O código implementa um consumidor de mensagens da fila RabbitMQ usando a biblioteca `pika`. A classe `PikaConsumer` herda de `PikaClient` e é responsável pela conexão e consumo das mensagens da fila. A seguir estão os principais pontos:

- A classe `PikaConsumer` se conecta ao RabbitMQ e começa a consumir as mensagens de uma fila específica.
- O método `on_message_received` é acionado sempre que uma mensagem é recebida. Ele faz o parsing da mensagem JSON, que contém a imagem codificada em Base64 e seus metadados (como o nome do arquivo), e chama a função de upload para o S3.
- O método `basic_ack` garante que a mensagem seja removida da fila após o processamento bem-sucedido.

### 2. Decodificação e Upload para o S3

A função `decode_and_upload` é responsável por:

- Decodificar a imagem que está em formato Base64.
- Salvar a imagem em um buffer de memória temporário no formato PNG.
- Enviar a imagem para um bucket S3, utilizando o cliente `boto3` para interação com o serviço de armazenamento da AWS.

### Detalhamento do código

#### 1. Conexão com o RabbitMQ:

A classe `PikaConsumer` herda de `PikaClient` e define a lógica para consumir mensagens:

```python
class PikaConsumer(PikaClient):
    def start_consumer(self):
        self._channel.basic_consume(
            queue=self._amqp_routing_key,
            on_message_callback=self.on_message_received,
            auto_ack=True
        )
        self._channel.start_consuming()
```

Aqui, a fila RabbitMQ é definida, e o método `start_consumer` inicia a escuta para mensagens na fila especificada. A opção `auto_ack=True` garante que as mensagens sejam confirmadas automaticamente após o recebimento.

#### 2. Processamento e Upload para o S3:

A função `decode_and_upload` realiza o trabalho pesado de decodificar a imagem e enviá-la ao S3:

```python
def decode_and_upload(base64_image: str, bucket_name: str, s3_file_name: str):
    image_data = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_data))
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    buffered.seek(0)
    
    session = boto3.Session()
    s3_client = boto3.client('s3')
    s3_client.upload_fileobj(buffered, bucket_name, s3_file_name, ExtraArgs={'ContentType': 'image/png'})
```

O fluxo acima decodifica a string Base64, carrega a imagem na memória e a armazena no formato PNG. O `boto3.client('s3')` é utilizado para enviar a imagem ao S3.

#### 3. Recepção da mensagem e decodificação:

No método `on_message_received`, a imagem Base64 e seus metadados são extraídos da mensagem recebida, decodificados e enviados ao S3:

```python
def on_message_received(self, channel, method, properties, body):
    message = json.loads(body.decode('utf-8'))
    decode_and_upload(message["image"], "bucket-greench", message["image_metadata"]["image_name"])
```

Neste exemplo, a mensagem é esperada em formato JSON e deve conter dois campos principais: a imagem codificada em Base64 e os metadados (nome do arquivo).

### Conclusão

Este serviço é uma parte essencial de um pipeline de processamento de imagens para contagem de árvores em regiões florestais. Ele integra uma solução baseada em nuvem e sistemas embarcados, onde imagens processadas localmente são enviadas para o S3 via RabbitMQ.

Este sistema garante que as imagens sejam armazenadas de forma segura e escalável, permitindo o uso de algoritmos avançados de visão computacional em etapas posteriores. O uso de boas práticas como logging detalhado e sessões AWS permite uma depuração eficiente, garantindo que erros de credenciais ou falhas de conexão sejam rapidamente identificados e corrigidos.