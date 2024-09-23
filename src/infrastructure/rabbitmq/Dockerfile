FROM rabbitmq:3.13.7-management-alpine

COPY rabbitmq.conf /etc/rabbitmq/

COPY definitions.json /etc/rabbitmq

RUN cat /etc/rabbitmq/rabbitmq.conf
