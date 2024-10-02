---
title: Análise financeira
sidebar_position: 4
--- 
# Análise financeira 

A análise financeira desempenha um papel fundamental na condução de decisões empresariais estratégicas e fundamentadas. Esse processo envolve a avaliação minuciosa de dados financeiros e econômicos, permitindo uma compreensão profunda da saúde financeira de uma organização, projeção de seu desempenho futuro e embasamento sólido para tomadas de decisões. Abrangendo uma variedade de aspectos, desde a avaliação de investimentos até o gerenciamento de riscos e otimização de recursos, essa análise é essencial para a sustentabilidade e crescimento de qualquer negócio.

A tabela a seguir apresenta uma estimativa dos gastos para um projeto de porte similar, com duração de um ano. Estes custos englobam despesas relacionadas aos funcionários, como salários e benefícios, ajustados conforme as leis trabalhistas vigentes. Também estão inclusos os valores relativos ao equipamento necessário para o projeto. Os números foram calculados com base em médias salariais para cada função, obtidas de fontes confiáveis como Catho Profissões e Glassdoor Salaries. Adicionalmente, as cifras foram adaptadas para refletir os custos associados à contratação em regime CLT, utilizando ferramentas como o iDinheiro, a fim de proporcionar uma estimativa precisa e alinhada com a realidade do mercado. 

## Tabela de Custos de Mão de Obra

| Cargo         | Salário Médio (mensal) | Horas Semanais | Duração (meses) | Custo Total |
| ------------- | ---------------------- | -------------- | --------------- | ----------- |
| Desenvolvedor Sênior | R$ 15.000,00              | 40               | 9               | R$ 135.000,00 |
| Desenvolvedor Pleno  | R$ 9.000,00               | 40               | 9               | R$ 81.000,00 |
| Desenvolvedor Júnior | R$ 5.000,00               | 40               | 9               | R$ 45.000,00 |

**Custo Total Mão de Obra**: R$ 261.000,00

---

## Tabela de Custos de Manutenção - Serviços AWS

Essa tabela de custos foi feita utilizando o período de tempo do projeto, ou seja, 9 meses. Além disso, para padronização da estimativa de preço, optou-se por converter o valor de dolár para real.

| Serviço| Custo Mensal | Descrição do Serviço                | Descrição de Uso                                        |
| -------| ------------ | ----------------------------------- | ------------------------------------------------------- |
| Amazon RDS - Quant(2)| 5,807.85 R$| Banco de dados relacional gerenciado| Hospedar banco de dados de alta disponibilidade (Postgres)|
| Amazon EC2 - Quant(5)| 220.22 R$  | Instâncias de computação elástica   | Servir o back-end e o front-end da aplicação            |
| Amazon S3  - Quant(1)| 22.77  R$  | Armazenamento escalável na nuvem    | Hospedar imagens e arquivos usados no sistema           |

**Custo Total de Manutenção (projeto todo)**: 54.486 R$

## Tabela de Custos de IoT:

A seguinte tabela apresenta os custos envolvidos para a compra do hardware necessário para o dispositivo na borda, composto principalmente pelo Raspberry Pi e o Drone.

| Item          | Descrição | Custo Total (R$) |
| ------------- | --------- | ---------------- |
| Raspberry Pi 5 8gb  | Microprocessador utilizado para a computação na borda | 980.00        |
| DJI Air 2S   | Drone utilizado para a coleta de imagens | 11,535.00           |
| Raspberry Pi AI Kit | Módulo de otimização de processamento de IA para o Raspberry Pi | 800.00        |
| Power Bank | Fonte de energia para o Raspberry Pi em 5V 5A | 700.00        |

**Custo Total de IoT**: 14.015 R$

### Resumo da configuração de cada serviço:
- **Amazon RDS** : Quantidade de armazenamento (100 GB), Nós (2), Tipo de instância (db.m1.large), Utilização (somente sob demanda) (100 %Utilized/Month), Opção de implantação (Multi-AZ), Modelo de preço (OnDemand), Volume de armazenamento (SSD de uso geral (gp2)), Custo de retenção por um mês (por vCPU/mês) (3.1098000000), Custo de cada mês adicional de retenção (por vCPU/mês) (0.1308000000), Custo de retenção total (por vCPU/mês) (4.16)

- **Amazon EC2** : Locação (Instâncias compartilhadas), Sistema operacional (Linux), Carga de trabalho (Consistent, Número de instâncias: 5), Instância do EC2 avançada (t3.micro), Pricing strategy (Compute Savings Plans 1yr No Upfront), Habilitar monitoramento (desabilitada), DT Entrada: Not selected (0 TB por mês), DT Saída: Not selected (0 TB por mês), DT Intrarregião: (0 TB por mês)

- **Amazon S3** : Armazenamento S3 Standard (100 GB por mês), Dados retornados pelo S3 Select (100 GB por mês)


## Conclusão

A análise financeira apresentada oferece uma visão abrangente dos custos envolvidos no desenvolvimento e manutenção de um projeto de tecnologia com duração de nove meses. Levando em consideração as despesas com mão de obra, serviços em nuvem (como AWS) e infraestrutura de IoT, foi possível obter uma estimativa precisa dos investimentos necessários. 

Com base nos dados apresentados, os custos totais, incluindo salários de desenvolvedores e os serviços da AWS, indicam que o projeto exige um investimento considerável, mas alinhado às necessidades técnicas e operacionais de um projeto desse porte. A projeção de custos, especialmente com mão de obra, reflete os valores de mercado e está ajustada conforme a legislação trabalhista vigente, enquanto os gastos com infraestrutura na nuvem foram calculados de acordo com o uso otimizado dos recursos da AWS.

Portanto, o custo final estimado para este projeto foi de XXXXX, ao longo de nove meses, oferece uma base sólida para a tomada de decisões estratégicas. Essa análise financeira demonstra a viabilidade do projeto, evidenciando a importância do planejamento financeiro detalhado para garantir o sucesso e a sustentabilidade do negócio, com foco em otimização de recursos e controle de despesas ao longo do desenvolvimento.