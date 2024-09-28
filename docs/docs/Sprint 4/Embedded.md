### Documentação do Sistema de Captura e Processamento de Imagens no Raspberry Pi 5

---

#### 1. **Descrição Geral do Sistema**
Este sistema foi projetado para capturar, processar e publicar informações sobre imagens capturadas por uma câmera USB conectada a um Raspberry Pi 5. Utiliza uma combinação de ferramentas de captura de imagem, processamento de imagens utilizando aprendizado profundo, mensageria para comunicação com outros serviços, e um pipeline de monitoramento para automação do fluxo.

O Raspberry Pi 5, com seu processador de múltiplos núcleos, é a infraestrutura ideal para gerenciar capturas de imagens em tempo real, executar modelos de Machine Learning compactos e gerenciar filas de mensagens para comunicação com outros sistemas.

---

#### 2. **Arquitetura do Sistema**
O sistema é composto por diferentes componentes:
- **Captura de Imagens**: Gerenciada pelo script `capture_handler.py` para capturar imagens da câmera conectada.
- **Monitoramento de Diretório**: `directory_monitor.py` verifica continuamente novos arquivos de imagem para processamento.
- **Processamento de Imagens**: `image_handler.py` utiliza um modelo Segformer para processar as imagens capturadas, gerando uma máscara de segmentação e metadados.
- **Publicação de Mensagens**: `publisher.py` utiliza o RabbitMQ para publicar os resultados das imagens processadas.
- **Worker**: `worker.py` integra todos os componentes, gerenciando o fluxo de captura, processamento e publicação.
- **Servidor**: `main.py` fornece uma interface para interagir com o sistema, permitindo que capturas e processamentos sejam disparados manualmente via API.

---

#### 3. **Instalação e Configuração no Raspberry Pi 5**
##### **Passos para Configuração do Sistema**
1. **Dependências**: Primeiro, é necessário instalar as dependências listadas no arquivo `requirements.txt`:
   ```sh
   pip install -r requirements.txt
   ```
2. **Variáveis de Ambiente**: Configure as variáveis de ambiente para o RabbitMQ no arquivo `.env`:
   - `AMQP_HOST`
   - `AMQP_PORT`
   - `AMQP_USERNAME`
   - `AMQP_PASSWORD`
3. **Câmera USB**: Conecte a câmera USB ao Raspberry Pi e certifique-se de que está funcionando corretamente.

---

#### 4. **Componentes e Funcionalidades**

##### **4.1. main.py**
Este é o script principal que inicializa o servidor FastAPI, fornecendo uma interface de API para disparar a captura e processamento das imagens. Também inicia o worker e o monitoramento de diretório em threads separadas, garantindo um fluxo contínuo.

##### **4.2. Capture Handler (`capture_handler.py`)**
Este script é responsável pela captura de imagens utilizando a biblioteca OpenCV. Ele:
- Acessa a câmera USB para capturar imagens.
- Salva as imagens capturadas no diretório especificado, com o nome baseado no timestamp (`IMG_YYYYMMDD-HHMMSS.jpg`).
- É configurado para rodar no Raspberry Pi 5, utilizando uma câmera USB, facilitando a captura em tempo real.

##### **4.3. Directory Monitor (`directory_monitor.py`)**
Monitora continuamente um diretório específico (`images`) em busca de novas imagens e as coloca em uma fila (`local_bus`) para processamento posterior. Ele:
- Monitora de forma contínua e envia as imagens para o próximo estágio (processamento).
- É configurado para verificar o diretório a cada 60 segundos.

##### **4.4. Image Handler (`image_handler.py`)**
Responsável pelo processamento das imagens usando um modelo Segformer. Este script:
- Carrega o modelo de segmentação Segformer (pré-treinado e ajustado para classes específicas).
- Gera máscaras de segmentação das imagens, calcula a área de cobertura e salva os metadados.
- Gera um JSON contendo informações como a máscara gerada, a área de cobertura e a imagem original codificada em Base64.

##### **4.5. Pika Client e Publisher (`client.py` e `publisher.py`)**
Esses scripts configuram e gerenciam a comunicação com o RabbitMQ:
- **PikaClient** (`client.py`) gerencia a conexão com o broker RabbitMQ.
- **PikaPublisher** (`publisher.py`) publica mensagens contendo informações das imagens processadas.

##### **4.6. Worker (`worker.py`)**
Este script gerencia o fluxo de trabalho, integrando os outros componentes:
- Inicia o monitoramento do diretório.
- Processa cada imagem assim que ela é detectada pelo monitoramento.
- Publica os resultados utilizando o PikaPublisher.
- Remove a imagem do diretório após processamento, garantindo um pipeline contínuo e limpo.

---

#### 5. **Mensageria e Logs**
- **Mensageria (RabbitMQ)**: As mensagens contendo informações sobre imagens processadas são enviadas via RabbitMQ. Isso permite que os resultados sejam distribuídos para outros sistemas, facilitando a integração em um ambiente maior.
- **Logs**: Utiliza uma classe customizada de logger (`logger.py`) para armazenar logs detalhados das operações. Os logs são salvos no diretório `logs/` e são fundamentais para monitoramento e depuração.

---

#### 6. **Infraestrutura no Raspberry Pi 5**
O Raspberry Pi 5 oferece uma excelente infraestrutura para este sistema devido aos seguintes pontos:
- **CPU Multinúcleo**: As threads do sistema (worker, servidor FastAPI, monitoramento de diretório) podem ser distribuídas eficientemente entre os núcleos do processador, garantindo performance otimizada.
- **USB 3.0**: A conectividade USB rápida facilita a captura e processamento de imagens em tempo real.
- **GPU Integrada**: Pode ser usada para aceleração de tarefas do modelo de Machine Learning, especialmente na parte de inferência com o modelo Segformer.
- **Conectividade de Rede**: A conectividade Ethernet ou WiFi permite que o Raspberry Pi 5 se comunique com o broker RabbitMQ, enviando informações processadas para outros sistemas.

---

#### 7. **Execução do Sistema**
Para iniciar o sistema, execute o script `main.py`:
```sh
python main.py
```
Este comando irá:
- Iniciar o monitoramento do diretório `images/` para novas capturas.
- Rodar um servidor FastAPI na porta 8000, possibilitando a interação com o sistema através de endpoints REST.
- Iniciar um worker para processar imagens e publicar os resultados.

---

#### 8. **Considerações Finais**
Este sistema foi projetado para funcionar de forma eficiente e autônoma, realizando a captura, o processamento, a publicação e o monitoramento de imagens em tempo real. A infraestrutura do Raspberry Pi 5 é amplamente adequada para garantir que todas as operações sejam realizadas sem atrasos significativos, maximizando a eficiência e a reatividade do sistema.