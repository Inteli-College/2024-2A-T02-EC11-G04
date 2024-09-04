# Base image para o RabbitMQ com o plugin de gerenciamento
FROM rabbitmq:3-management

# Definir variáveis de ambiente para RabbitMQ
ENV RABBITMQ_DEFAULT_USER=grupo4
ENV RABBITMQ_DEFAULT_PASS=grupo4
ENV RABBITMQ_HOST=localhost
ENV RABBITMQ_PORT=5672

# Expor as portas do RabbitMQ
EXPOSE 5672 15672

# Comando para iniciar o RabbitMQ
CMD ["rabbitmq-server"]