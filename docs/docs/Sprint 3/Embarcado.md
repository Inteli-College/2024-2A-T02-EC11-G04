# Fluxo e estrutura de dados no embarcado

## Descrição Geral
Este projeto tem como objetivo a identificação de regiões florestais e contagem de árvores por meio de um sistema embarcado, utilizando o **Raspberry Pi**. O projeto processa imagens através de um modelo de segmentação semântica que identifica as árvores em cada imagem. As imagens processadas e seus metadados são enviados para uma fila **RabbitMQ**, onde outros sistemas podem realizar processamento adicional ou armazenamento.

O projeto foi organizado de maneira modular, com o objetivo de facilitar a manutenção, o processamento distribuído e a reutilização de componentes. Utiliza uma abordagem de processamento assíncrono para monitorar um diretório local de imagens, processá-las e enviá-las para uma fila de mensagens.

## Estrutura da Pasta

```bash
src/
    embedded/
        logs/
        messaging/
            __init__.py
            client.py
            publisher.py
        utils/
            __init__.py
            directory_monitor.py
            image_handler.py
            logger.py
        worker/
            __init__.py
            worker.py
        Dockerfile
        main.py
```

## Descrição dos Arquivos e Principais Funções

### 1. messaging/

- **`__init__.py`**: Contém os metadados do pacote `messaging`, como a versão.

- **`client.py`**: Define a classe `PikaClient`, responsável por gerenciar a conexão com o RabbitMQ. Principais métodos:
  - **`connect_to_broker`**: Estabelece uma conexão com o broker RabbitMQ usando as credenciais definidas no arquivo `.env`.
  - **`disconnect_from_broker`**: Fecha a conexão com o RabbitMQ.

- **`publisher.py`**: Define a classe `PikaPublisher`, que herda de `PikaClient` e publica mensagens na fila RabbitMQ. Métodos principais:
  - **`publish_message`**: Publica uma mensagem no RabbitMQ. Usa o `BasicProperties` para garantir que a mensagem seja persistente.

### 2. utils/

- **`__init__.py`**: Contém os metadados do pacote `utils` e realiza a importação dos módulos `DirectoryMonitor`, `ImageHandler` e `Logger`.

- **`directory_monitor.py`**: Define a classe `DirectoryMonitor`, responsável por monitorar continuamente um diretório em busca de novas imagens. Funções principais:
  - **`start_monitoring`**: Inicia o monitoramento do diretório em uma thread separada.
  - **`processing_images_bus`**: Adiciona as imagens encontradas em um diretório à fila local para processamento.

- **`image_handler.py`**: Define a classe `ImageHandler`, que processa as imagens para envio. Funções principais:
  - **`process_image`**: Converte uma imagem para base64 e gera os metadados em formato JSON.

- **`logger.py`**: Define a classe `Logger`, que cria e configura um logger para gerar logs personalizados. Função principal:
  - **`_get_logger`**: Retorna a instância configurada do logger.

### 3. worker/

- **`__init__.py`**: Define os metadados do pacote `worker`.

- **`worker.py`**: Define a classe `Worker`, responsável por coordenar o processo de monitoramento, compressão e envio das imagens para o RabbitMQ. Principais funções:
  - **`run`**: Inicia o loop principal que verifica o diretório monitorado, processa as imagens e publica as mensagens na fila RabbitMQ.
  - **`start_thread`**: Inicia o worker em uma thread separada.

### 4. Dockerfile

O **Dockerfile** define o ambiente de execução do projeto, utilizando a imagem base `python:3.12-slim-bookworm`. Principais etapas:

- Definição do diretório de trabalho (`WORKDIR /worker`).
- Instalação das dependências via `pip` utilizando o arquivo `requirements.txt`.
- Comando para execução do script principal: `CMD ["python", "main.py"]`.

### 5. main.py

O arquivo principal que inicializa o sistema. Ele cria uma instância do `DirectoryMonitor` e do `ImageHandler`, além de instanciar múltiplos workers para processar as imagens em paralelo.

---

## Como Usar

### Requisitos

- Python 3.12 ou superior
- Docker (opcional para rodar em contêiner)
- RabbitMQ

### Passos

1. Clone o repositório:

   ```bash
   git clone <url-do-repositorio>
   cd src/embedded
    ```

2. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure o arquivo `.env` com as variáveis de ambiente para o RabbitMQ:

    ```bash
    AMQP_HOST=seu_host
    AMQP_PORT=sua_porta
    AMQP_USERNAME=seu_usuario
    AMQP_PASSWORD=sua_senha
    AMQP_EXCHANGE=seu_exchange
    AMQP_ROUTING_KEY=sua_routing_key
    ```
4. Para rodar o projeto com Docker:

    ```bash
    docker build -t tree-count .
    docker run -d tree-count
    ```

5. Para rodar o projeto localmente:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python main.py
    ```

O sistema monitorará o diretório images/, processará as imagens e enviará os dados para o RabbitMQ automaticamente.

## Logs

Os logs do sistema são gravados no diretório `logs/`, com arquivos nomeados de acordo com a data e hora de execução do sistema. Eles contêm informações sobre a execução do worker, incluindo o status de cada imagem processada e erros, caso ocorram.

## Conclusão

Este sistema foi projetado para ser altamente modular e extensível, permitindo fácil integração com outros sistemas e adaptação para diferentes cenários de processamento de imagem. Com a abordagem de filas assíncronas do RabbitMQ, o sistema pode escalar para múltiplos consumidores e ser integrado em pipelines mais complexos de análise de imagens e dados ambientais.

