import pika

import sys

from client import PikaClient
from utils import Logger  

_logger = Logger(__name__)._get_logger()


class PikaConsumer(PikaClient):
    def __init__(self):
        super().__init__()
        self._channel = self.connect_to_broker()

    def on_message_received(self, channel, method, properties, body) -> None:
        _logger.info("Message received: %s", body)

    def start_consumer(self):
        self._channel.basic_consume(queue=self._amqp_routing_key,
                                    on_message_callback=self.on_message_received,
                                    auto_ack=False)
        self._channel.start_consuming()

def main():
    pika_consumer=PikaConsumer()
    pika_consumer.start_consumer()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        _logger.info("Shutting down workers...")
        sys.exit(0)
