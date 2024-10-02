from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.exceptions import AMQPChannelError, AMQPConnectionError
from dotenv import load_dotenv

load_dotenv()

import os


class PikaClient:
    """Sets up a basic client to interact with RabbitMQ."""
    def __init__(self) -> None:
        self._connection = None
        self._channel = None
        self._stopping = False
        
        self._amqp_host = os.getenv("AMQP_HOST")
        self._amqp_vhost = os.getenv("AMQP_VHOST")
        self._amqp_port = os.getenv("AMQP_PORT")
        self._amqp_username = os.getenv("AMQP_USERNAME")
        self._amqp_password = os.getenv("AMQP_PASSWORD")
        self._amqp_exchange = os.getenv("AMQP_EXCHANGE")
        self._amqp_routing_key = os.getenv("AMQP_ROUTING_KEY")
        print(self._amqp_host)
        print(type(self._amqp_host))

    def connect_to_broker(self):
        """Returns a channel object from pika to interact with RabbitMQ.

        Returns:
            pika.channel.Channel: A RabbitMQ channel object.
        """
        print("Connecting to broker")
        try:
            credentials = PlainCredentials(
                self._amqp_username,
                self._amqp_password
            )
            parameters = ConnectionParameters(
                host=self._amqp_host,
                virtual_host=self._amqp_vhost,
                port=self._amqp_port,
                credentials=credentials,
                connection_attempts=5,
                retry_delay=5,
                heartbeat=30
            )
            self._connection = BlockingConnection(parameters)
            self._channel = self._connection.channel()
            print("Connected to broker")
            return self._channel
        except (AMQPConnectionError, AMQPChannelError) as e:
            print("Failed to connect to broker with error: %s",
                        str(e))
            raise e

    def disconect_from_broker(self, stopping_flag: bool = False):
        print("Disconnecting from broker")
        self._stopping = stopping_flag
        if self._connection.is_open and self._stopping:
            self._connection.close()
        print("Disconnected from broker, connection closed")
