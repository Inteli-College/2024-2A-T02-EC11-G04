from pika import BasicProperties
from pika.exceptions import AMQPChannelError

from .client import PikaClient
from utils import Logger

_logger = Logger(logger_name=__name__)._get_logger()


class PikaPublisher(PikaClient):
    """Handles the publishing of messages to RabbitMQ using the PikaClient."""

    def __init__(self) -> None:
        """Initializes the publisher with a PikaClient instance.

        Args:
            pika_client (PikaClient): A configured PikaClient instance for managing connections.
        """
        super().__init__()
        self._channel = self.connect_to_broker()

    def publish_message(self, message: str):
        """Publishes a message to the given exchange with the specified routing key.

        Args:
            exchange (str): The RabbitMQ exchange to which the message will be sent.
            routing_key (str): The routing key for the message (queue_name).
            message (str): The message to be sent.
        """
        if self._channel is None or not self._channel.is_open:
            _logger.error("Failed to publish message: Channel is not open.")
            raise AMQPChannelError("Channel is not open.")

        try:
            self._channel.basic_publish(
                exchange=self._amqp_exchange,
                routing_key=self._amqp_routing_key,
                body=message,
                properties=BasicProperties(
                    delivery_mode=2
                )
            )
            _logger.info("Message published successfully.")
        except Exception as e:
            _logger.error("Failed to publish message with error: %s",
                        str(e))
            return e 
