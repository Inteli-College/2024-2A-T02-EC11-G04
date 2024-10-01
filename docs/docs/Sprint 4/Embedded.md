---
title: Embarcado
sidebar_position: 2
---

### Documentação do Sistema de Captura e Processamento de Imagens no Raspberry Pi 5

---

#### 1. **Descrição Geral do Sistema**
Este sistema foi projetado para capturar, processar e publicar informações sobre imagens obtidas por uma câmera USB conectada ao Raspberry Pi 5. Utiliza uma combinação de ferramentas de captura de imagem, processamento de imagens com um modelo Segformer pré-treinado, mensageria para comunicação eficiente e um pipeline de monitoramento automatizado. O Raspberry Pi 5, com seu processador multicore e suporte a GPU, é uma plataforma ideal para executar este sistema de maneira eficiente.

---

#### 2. **Arquitetura do Sistema**
O sistema é composto por componentes altamente modularizados, permitindo uma integração limpa e a possibilidade de melhorias incrementais:
- **Captura de Imagens**: Gerenciada pelo script `capture_handler.py`, que utiliza OpenCV para interagir com a câmera.
- **Monitoramento de Diretório**: `directory_monitor.py` observa continuamente novos arquivos de imagem para processamento.
- **Processamento de Imagens**: `image_handler.py` utiliza aprendizado profundo para processar as imagens.
- **Mensageria**: Utiliza RabbitMQ para enviar os dados processados a outros sistemas.
- **Worker e Coordenação de Fluxo**: `worker.py` integra os componentes, garantindo a automação do ciclo de vida das imagens, desde a captura até a publicação.
- **Servidor**: `main.py` fornece uma interface para interagir com o sistema, permitindo que capturas e processamentos sejam disparados manualmente via API.

Cada componente é implementado de maneira independente, o que facilita a manutenção e a evolução do sistema.

---

#### 3. **Instalação e Configuração no Raspberry Pi 5**
##### **Passos para Configuração do Sistema**
1. **Dependências**: Primeiro, instale as dependências listadas no arquivo `requirements.txt`:
   ```sh
   pip install -r requirements.txt
   ```
2. **Configuração do Ambiente**:
   - Configure as variáveis de ambiente no arquivo `.env`. Estas variáveis são essenciais para estabelecer a comunicação com o broker RabbitMQ:
     - `AMQP_HOST`: IP/URL do broker RabbitMQ.
     - `AMQP_PORT`: Porta de comunicação (padrão 5672).
     - `AMQP_USERNAME` e `AMQP_PASSWORD`: Credenciais de acesso.
     - `AMQP_EXCHANGE` e `AMQP_ROUTING_KEY`: Configurações para o intercâmbio de mensagens.
3. **Câmera USB**: Conecte a câmera USB ao Raspberry Pi. Verifique seu funcionamento executando um teste simples com OpenCV (`cv2.VideoCapture()`).

##### **Configuração Avançada**
- **Configurações de Diretórios**: O caminho padrão de saída das imagens é `images/`. Caso queira alterá-lo, ajuste a variável `OUTPUT_DIRECTORY` no `.env` ou modifique diretamente os scripts.
- **Rede**: Recomenda-se que o Raspberry Pi esteja conectado via Ethernet para garantir uma conexão estável, especialmente durante a comunicação com o broker RabbitMQ.

---

#### 4. **Componentes e Funcionalidades**

##### **4.1. main.py**
Este é o script principal que orquestra a execução do sistema:
- **Servidor FastAPI**: Inicializa um servidor REST que permite capturar novas imagens ou processar uma imagem já existente através de chamadas HTTP (`/capture-image` e `/process-image/{image_name}`).
- **Inicia Threads Paralelas**: O monitoramento do diretório e o worker são executados em threads separadas, garantindo que o processamento seja contínuo e que a API esteja sempre disponível.

##### **4.2. Capture Handler (`capture_handler.py`)**
- **Captura de Imagens**: Utiliza a biblioteca OpenCV para acessar a câmera USB e capturar imagens com resolução ajustável (padrão 640x480).
- **Nomenclatura Baseada em Timestamps**: Gera nomes de arquivos baseados no timestamp para facilitar o rastreamento e evitar conflitos de nomes.

##### **4.3. Directory Monitor (`directory_monitor.py`)**
- **Monitoração em Tempo Real**: Monitora o diretório `images/` e coloca novas imagens em uma fila (`local_bus`) para processamento. 
- **Thread de Monitoramento**: A função `start_monitoring()` inicia uma thread daemon para monitoramento contínuo, o que evita bloquear o funcionamento do sistema principal.
- **Tratamento de Conflitos**: Evita adicionar arquivos temporários ou corrompidos, ignorando arquivos que começam com um ponto (`.`).

##### **4.4. Image Handler (`image_handler.py`)**
- **Processamento com Aprendizado Profundo**: Utiliza o Segformer para realizar segmentação semântica da imagem.
- **Modelo Personalizado**: Carrega pesos pré-treinados específicos e realiza inferências para segmentar árvores (ou outros elementos).
- **Geração de Metadados**: Gera um JSON contendo a máscara gerada, a área da máscara (em pixels e percentual) e a imagem original em Base64. Isso facilita a integração com outros sistemas que precisam de informações detalhadas sobre a imagem.

##### **4.5. Pika Client e Publisher (`client.py` e `publisher.py`)**
- **PikaClient**: Estabelece e gerencia a conexão com o broker RabbitMQ. Suporta reconexões automáticas em caso de falha.
- **PikaPublisher**: Herda do `PikaClient` e adiciona a funcionalidade de publicar mensagens. Publica os dados das imagens processadas na troca e fila configuradas.

##### **4.6. Worker (`worker.py`)**
- **Ciclo de Vida da Imagem**: Inicia o monitoramento do diretório, processa cada imagem e publica os resultados. Após a publicação, a imagem é removida para evitar reprocessamento.
- **Fluxo Automatizado**: Todos os passos são coordenados de forma assíncrona, garantindo que o sistema continue funcionando mesmo se uma imagem específica falhar no processamento.

---

#### 5. **Mensageria e Logs**
- **Mensageria (RabbitMQ)**: Utiliza o RabbitMQ para comunicação entre diferentes partes do sistema ou para enviar resultados para outros serviços. Esse mecanismo permite escalabilidade, pois outros consumidores podem ser adicionados ao sistema para lidar com volumes crescentes.
- **Logs Detalhados**: Os logs fornecem detalhes de cada etapa do fluxo, desde a captura de imagens até a publicação dos resultados. Eles são salvos no diretório `logs/` e contêm informações sobre:
  - **Conexões de Mensageria**: Registra falhas e sucessos ao conectar ao RabbitMQ.
  - **Eventos de Monitoramento e Processamento**: Informações detalhadas sobre cada imagem processada, incluindo erros que possam ocorrer.

---

#### 6. **Infraestrutura no Raspberry Pi 5**
O Raspberry Pi 5 é fundamental para o desempenho deste sistema, e várias características do hardware são aproveitadas:
- **CPU Multinúcleo**: A capacidade de processamento em paralelo do Raspberry Pi 5 permite que o monitoramento, captura de imagens, e execução do servidor FastAPI ocorram simultaneamente, maximizando a eficiência do sistema.
- **GPU Integrada**: Utilizar a GPU para inferência pode acelerar significativamente o processamento das imagens, especialmente ao rodar o modelo Segformer para segmentação.
- **USB 3.0**: A conectividade USB rápida permite que imagens de alta resolução sejam capturadas sem atrasos, garantindo que o sistema possa responder rapidamente a mudanças no ambiente.
- **Suporte à Rede**: A conectividade de alta velocidade (Ethernet ou WiFi) é essencial para garantir que o Raspberry Pi consiga enviar as informações processadas ao broker RabbitMQ com confiabilidade.

---

#### 7. **Tratamento de Erros e Recuperação**
- **Erros de Conexão ao RabbitMQ**: Em `client.py`, ao falhar a conexão, uma nova tentativa é feita utilizando `connection_attempts` e `retry_delay`. Caso não consiga se conectar após o número de tentativas, a falha é registrada nos logs.
- **Captura de Imagem Falha**: O `capture_handler.py` verifica se a câmera foi corretamente inicializada antes de prosseguir. Caso contrário, exibe uma mensagem de erro e encerra a tentativa de captura.
- **Monitoramento do Diretório**: Em `directory_monitor.py`, caso ocorra um erro durante o monitoramento, o sistema espera um período definido (`poll_interval`) antes de retomar, garantindo que erros transitórios não causem interrupções permanentes.

---

#### 8. **Execução do Sistema**
Para iniciar o sistema, execute o script `main.py`:
```sh
python main.py
```
Este comando irá:
- **Iniciar o Monitoramento do Diretório**: A thread de monitoramento buscará novas imagens para processar.
- **Rodar o Servidor FastAPI**: A API estará disponível na porta 8000, possibilitando o controle da captura e processamento.
- **Iniciar o Worker**: O worker será responsável por pegar as imagens da fila, processá-las e enviar os dados para o RabbitMQ.

---

#### 9. **Fluxo de Mensagens e Logs**
- **Ciclo de Vida das Mensagens**:
  1. **Captura**: A imagem é capturada e salva no diretório monitorado.
  2. **Monitoramento e Processamento**: Aimagem é identificada pelo monitoramento e processada, gerando uma máscara e metadados.
  3. **Publicação**: O resultado é publicado no RabbitMQ, podendo ser consumido por outro sistema.

- **Logs**:
  - Logs detalham cada ação realizada no ciclo de vida da imagem.
  - Logs de erros são gerados em cada estágio para facilitar a depuração.

---

#### 10. **Considerações Finais e Ideias de Melhorias Futuras**
##### **Escalabilidade**
- **Distribuição dos Workers**: Em vez de rodar um único worker no Raspberry Pi 5, temos a possibilidade de distribuir o processamento em múltiplos dispositivos. Isso poderia ser feito utilizando filas do RabbitMQ para gerenciar melhor as imagens em ambientes com alta demanda.
- **Melhoria de Performance do Modelo**:  Quantizar o modelo Segformer para otimizar a inferência no Raspberry Pi, reduzindo o uso de memória e aumentando a velocidade.

##### **Otimizações de Hardware**
- **Uso da GPU do Raspberry Pi**: Explorar bibliotecas que suportem a GPU do Raspberry Pi para acelerar o processamento das imagens.
- **Redução de Carga da CPU**: Offload de operações de pre-processamento de imagem para a GPU.

##### **Integração com Cloud**
- **Sincronização com Serviços Cloud**: Para aumentar a capacidade de armazenamento e processamento, vamos sincronizar as imagens e metadados com serviços na nuvem (ex. AWS S3, AWS RDS).