---
title: Setup
sidebar_position: 2
---

# Setup Raspberry Pi 5

## Introdução

Este guia tem como objetivo auxiliar na configuração do Raspberry Pi 5 para execução de modelos de detecção de árvores. Para isso, vamos abordar os seguintes tópicos:

1. **Instalação do Sistema Operacional**: Passo a passo para instalar o sistema operacional Raspberry Pi OS no cartão SD.
2. **Configuração Inicial**: Inicialização do Raspberry Pi e configuração de ajustes básicos.
3. **Instalação de Dependências**: Instalação de bibliotecas e ferramentas necessárias para execução de modelos de detecção de objetos.

## Instalação do Sistema Operacional

Para essa solução, foi escolhido o sistema operacional Ubuntu Server 24.04 LTS. Essa escolha foi feita devido a sua compatibilidade com a arquitetura ARM e por ser uma versão LTS, que garante suporte a longo prazo. Além disso, o Ubuntu Server é uma versão mais leve e otimizada para servidores, o que é ideal para o Raspberry Pi.

Para realizar a instalação do Ubuntu Server no Raspberry Pi, siga os passos abaixo:

1. **Instalação do Raspberry Pi Imager**: Baixe e instale o [Raspberry Pi Imager](https://www.raspberrypi.org/software/).
2. **Escolha do Sistema Operacional**: Abra o Raspberry Pi Imager e escolha a opção "Ubuntu Server 24.04 LTS (Raspi)".
3. **Seleção do Cartão SD**: Insira o cartão SD no seu computador e selecione-o no Raspberry Pi Imager.
4. **Edição das Configurações**: Caso deseje, você pode editar as configurações do sistema operacional antes de gravá-lo no cartão SD. Clique em "Ctrl+Shift+X" para abrir o editor de configurações. Sendos os principais parâmetros:
   - **Network Configuration**: Configuração da rede, como Wi-Fi e IP estático.
   - **User Configuration**: Configuração do usuário e senha.
   - **SSH Configuration**: Habilitação do SSH.
5. **Gravação no Cartão SD**: Clique em "Write" para gravar o sistema operacional no cartão SD.

Após a gravação, insira o cartão SD no Raspberry Pi e ligue-o. O Ubuntu Server será inicializado e você poderá prosseguir com a configuração inicial.

## Configuração Inicial

Após a inicialização do Ubuntu Server no Raspberry Pi, siga os passos abaixo para a configuração inicial:

1. **Login**: Faça login no Raspberry Pi com o usuário e senha configurados durante a instalação.
2. **Atualização do Sistema**: Execute o comando abaixo para atualizar o sistema:

```bash
sudo apt update && sudo apt upgrade -y
```

3. **Configuração da Rede**: Caso não tenha configurado a rede durante a instalação, você pode configurá-la manualmente editando o arquivo `/etc/netplan/50-cloud-init.yaml`:

```yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: true
      optional: true
```

4. **Habilitação do SSH**: Caso não tenha habilitado o SSH durante a instalação, você pode habilitá-lo com o comando:

```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

5. **Configuração do Hostname**: Edite o arquivo `/etc/hostname` e adicione o nome desejado para o Raspberry Pi.

6. **Reinicialização**: Após realizar as configurações, reinicie o Raspberry Pi com o comando:

```bash
sudo reboot
```

Com essas configurações iniciais, o Raspberry Pi estará pronto para a instalação das dependências necessárias para execução de modelos de detecção de objetos.
