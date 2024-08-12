---
title: Levantamento de Requisitos
sidebar_position: 1
slug: /requirements-gathering
---

Para garantir que o projeto atenda às necessidades do cliente, identificadas durante uma entrevista de levantamento de aprimoramento de entendimento do projeto, os requisitos foram divididos em duas categorias principais: funcionais e não funcionais. Essa divisão foi motivada pela complexidade do projeto, que demanda tanto a implementação de funcionalidades específicas conforme os requisitos mínimos estabelecidos quanto o cumprimento de métricas de desempenho. Dentro dessas categorias, os Requisitos Funcionais (RFs) descrevem o que o sistema deve realizar, enquanto os Requisitos Não Funcionais (RNFs) estabelecem as métricas de desempenho a serem alcançadas pelos requisitos funcionais. Cada requisito foi ainda classificado como "obrigatório" ou "desejável", permitindo à equipe de desenvolvimento estabelecer uma ordem de prioridade para sua implementação.

## Requisitos Funcionais

| ID   | Título                                    | Descrição                                                                                           | Categoria   |
|------|-------------------------------------------|-----------------------------------------------------------------------------------------------------|-------------|
| RF1  | Detecção e Contagem Automática de Árvores | O sistema deve ser capaz de identificar e contar automaticamente o número de árvores em uma imagem capturada por satélites ou drones. | Obrigatório |
| RF2  | Visualização de Resultados em Dashboard   | O sistema deve fornecer uma interface de dashboard onde os usuários possam visualizar a quantidade de árvores por região em imagens de satélite ou drone. | Obrigatório |
| RF3  | Classificação de Árvores por Espécie      | O modelo deve ser capaz de classificar árvores por espécies, com base nas características físicas observadas nas imagens. | Desejável   |
| RF4  | Relatórios de Rastreabilidade             | O sistema deve permitir a geração de relatórios que incluem timelapses das áreas monitoradas, necessários para certificações como a VM0047. | Obrigatório |
| RF5  | Armazenamento e Consulta de Imagens       | As imagens utilizadas para a detecção devem ser armazenadas para futuras consultas e análises, possibilitando rastreabilidade e verificação histórica. | Obrigatório |
| RF6  | Delimitação por Hectares                  | O sistema deve permitir a contagem de árvores por hectare, considerando a densidade esperada (2000 - 2500 árvores por hectare). | Desejável   |
| RF7  | Integração com Portais de Transparência   | O sistema deve integrar-se a um portal de transparência, permitindo que consumidores e stakeholders visualizem informações detalhadas sobre as áreas reflorestadas. | Desejável   |

## Requisitos Não Funcionais

| ID   | Título                                | Descrição                                                                                                       | Métrica                                                                                                         | Categoria   |
|------|---------------------------------------|-----------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|-------------|
| RNF1 | Precisão do Modelo                    | O modelo de deep learning deve alcançar uma precisão de detecção e contagem de árvores de pelo menos 90-95%.    | Taxa de acurácia ≥ 90% em testes com imagens de validação.                                                       | Obrigatório |
| RNF2 | Desempenho em Edge Computing          | O sistema deve ser otimizado para rodar em dispositivos móveis e sistemas embarcados, garantindo uma latência mínima durante a análise das imagens. | Tempo de resposta médio ≤ 2 segundos para análises em dispositivos embarcados.                                   | Obrigatório |
| RNF3 | Escalabilidade                        | O sistema deve ser capaz de escalar para processar grandes volumes de dados provenientes de diferentes áreas geográficas. | Capacidade de processamento deve suportar o crescimento de usuários e dados em pelo menos 50% ao longo de um ano. | Desejável   |
| RNF4 | Segurança e Privacidade               | As informações armazenadas, incluindo imagens e dados de localização, devem ser protegidas por mecanismos de segurança adequados. | Nenhuma violação de segurança detectada durante auditorias periódicas.                                           | Obrigatório |
| RNF5 | Usabilidade e Interface de Usuário    | A interface do sistema deve ser intuitiva e fácil de usar, permitindo que usuários sem conhecimento técnico avancado possam interpretar os resultados com facilidade. | Taxa de conclusão de tarefas pelos usuários ≥ 90% sem necessidade de suporte adicional.                          | Desejável   |
| RNF6 | Resiliência a Variações Ambientais    | O modelo deve ser robusto o suficiente para lidar com variações ambientais, garantindo a consistência dos resultados. | Taxa de erro < 5% em diferentes condições de luz, tipos de solo e relevo.                                        | Obrigatório |

