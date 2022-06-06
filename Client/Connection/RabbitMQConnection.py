import json
from abc import ABC

import pika
from configparser import ConfigParser, ExtendedInterpolation


class RabbitMQConnection:
    @staticmethod
    def from_config():
        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read('config.ini')

        return RabbitMQConnection(
            config['RABBITMQ'].get('address'),
            config['RABBITMQ'].get('port'),
            config['RABBITMQ'].get('username'),
            config['RABBITMQ'].get('password'),
            config['RABBITMQ'].get('queue_prefix')
        )

    def __init__(self, server, port, username, password, queue_prefix):
        params = pika.ConnectionParameters(
            server,
            credentials=pika.PlainCredentials(username, password),
            port=port,
            heartbeat=5000
        )
        self._connection = pika.BlockingConnection(params)
        self._channel = self._connection.channel()
        self.__queue_prefix = queue_prefix

    def send_message(self, exchange, queue, body):
        print(f'dispatching query to {exchange}@{queue}')
        self._channel.basic_publish(exchange=exchange, routing_key=queue, body=body)

    def await_single_response(self, queue):
        result = ''

        def cb(ch, method, properties, body):
            nonlocal result
            result = body
            self._channel.stop_consuming()

        self._channel.basic_consume(queue=f'{self.__queue_prefix}.{queue}', on_message_callback=cb, auto_ack=True)
        self._channel.start_consuming()

        return json.loads(result)

    def await_messages(self, queue, callback):
        print(f'Listening to {self.__queue_prefix}.{queue}')
        self._channel.basic_consume(queue=f'{self.__queue_prefix}.{queue}', on_message_callback=callback, auto_ack=True)
        self._channel.start_consuming()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._connection:
            self._connection.close()


class WithDefaultRabbitMQConnection(ABC):
    def __init__(self):
        config = ConfigParser()
        config.read('config.ini')
        self.__exchange = config['RABBITMQ'].get('exchange')
        self.__queue_prefix = config['RABBITMQ'].get('queue_prefix')
