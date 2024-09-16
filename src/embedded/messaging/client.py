from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.exceptions import AMQPConnectionError, AMQPChannelError
from dotenv import load_dotenv

import os

from utils import Logger

load_dotenv()
_logger=Logger(logger_name=__name__)._get_logger()


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
        # Quick way to check if the environment variables are being loaded
        #region Debugging 
        # _logger.debug("""
        # Publisher initialized with the following connection parameters:
        # Host: %s
        # VHost: %s
        # Port: %s
        # Virtual Host: %s
        # Username: %s
        # Exchange: %s
        # Routing Key: %s
        # """,
        #             self._amqp_host,
        #             self._amqp_vhost,
        #             self._amqp_port,
        #             self._amqp_password,
        #             self._amqp_username,
        #             self._amqp_exchange,
        #             self._amqp_routing_key
        #             )
        #endregion

    def connect_to_broker(self):
        """Returns a channel object from pika to interact with RabbitMQ.

        Returns:
            pika.channel.Channel: A RabbitMQ channel object.
        """
        _logger.info("Connecting to broker")
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
                heartbeat=0
            )
            self._connection = BlockingConnection(parameters)
            self._channel = self._connection.channel()
            _logger.info("Connected to broker")
            return self._channel
        except (AMQPConnectionError, AMQPChannelError) as e:
            _logger.error("Failed to connect to broker with error: %s",
                        str(e))
            return e

    def disconect_from_broker(self, stopping_flag: bool = False):
        _logger.info("Disconnecting from broker")
        self._stopping = stopping_flag
        if self._connection.is_open and self._stopping:
            self._connection.close()
        _logger.info("Disconnected from broker, connection closed")
