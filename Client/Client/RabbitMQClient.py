import json
from configparser import ConfigParser, ExtendedInterpolation

from Connection import RabbitMQConnection
from Message import RabbitMQMessage, RabbitMQResponse


class RabbitMQQueryDispatcher:
    def __init__(self):
        config = ConfigParser()
        config.read('config.ini')
        self.__exchange = config['RABBITMQ'].get('exchange')
        self.__result_queue = config['QUEUES'].get('result_queue')

    def dispatch_query(self, query: RabbitMQMessage):
        with RabbitMQConnection.from_config() as rmc:
            queue, message = self.__parse_query(query)
            rmc.send_message(self.__exchange, queue, message)
            return rmc.await_single_response(self.__result_queue)

    def __parse_query(self, query: RabbitMQMessage):
        queue = f'{query.topic()}'
        message = query.json()
        return queue, message


class RabbitMQQueryListener:
    def __init__(self, queue_config):
        config = ConfigParser()
        config.read('config.ini')
        self.__exchange = config['RABBITMQ'].get('exchange')
        self.__connection = RabbitMQConnection.from_config()
        self.__result_queue = config['QUEUES'].get('result_queue')
        self.__queue_name = config['QUEUES'].get(queue_config)

    def listen(self, callback):
        self.__connection.await_messages(self.__queue_name, callback)

    def respond(self, message: RabbitMQResponse):
        self.__connection.send_message(self.__exchange, self.__result_queue, message.json())

# class RabbitMQProducer(RabbitMQConnection):
#     @staticmethod
#     def from_config():
#         config = ConfigParser(interpolation=ExtendedInterpolation())
#         config.read('config.ini')
#         rabbit = config['RABBITMQ']
#
#         return RabbitMQProducer(
#             rabbit.get('address'),
#             rabbit.get('port'),
#             rabbit.get('username'),
#             rabbit.get('password'),
#         )
#
#     def __init__(self, server, port, username, password):
#         params = pika.ConnectionParameters(server, credentials=pika.PlainCredentials(username, password),
#                                            port=port, heartbeat=5000)
#         self._connection = pika.BlockingConnection(params)
#         self._channel = self._connection.channel()
#
#     def publish(self, exchange, topic, data):
#         self._channel.basic_publish(exchange=exchange, routing_key=topic, body=data)
#
#     def publish_rmq_message(self, message: RabbitMQMessage):
#         self._channel.basic_publish(exchange=message.exchange(), routing_key=message.topic(), body=message.json())
#
#
# class RabbitMQConsumer(RabbitMQConnection, ABC):
#     _exchange: str
#     _queue: str
#
#
#
#     def __init__(self, server, port, exchange, queue, username, password):
#         params = pika.ConnectionParameters(server, credentials=pika.PlainCredentials(username, password), port=port, heartbeat = 300)
#         self._connection = pika.BlockingConnection(params)
#         self._channel = self._connection.channel()
#         self._exchange = exchange
#         self._queue = queue
#
#     def stop_consuming(self):
#         self._channel.stop_consuming()
#
#     @abstractmethod
#     def consume(self, callback): ...
#
#
# class RabbitMQSyncConsumer(RabbitMQConsumer):
#     @staticmethod
#     def from_config(queue_name: str):
#         config = ConfigParser(interpolation=ExtendedInterpolation())
#         config.read('config.ini')
#         rabbit = config['RABBITMQ']
#
#         return RabbitMQSyncConsumer(
#             rabbit.get('address'),
#             rabbit.get('port'),
#             rabbit.get('exchange'),
#             config.get('QUEUES', queue_name),
#             rabbit.get('username'),
#             rabbit.get('password'),
#         )
#
#     def consume(self, callback):
#             self._channel.basic_consume(queue=self._queue, on_message_callback=callback, auto_ack=True)
#         self._channel.start_consuming()
#
#
# class RabbitMQAsyncConsumer(RabbitMQConsumer):
#
#     @staticmethod
#     def from_config(queue_name: str):
#         config = ConfigParser(interpolation=ExtendedInterpolation())
#         config.read('config.ini')
#         rabbit = config['RABBITMQ']
#
#         return RabbitMQAsyncConsumer(
#             rabbit.get('address'),
#             rabbit.get('port'),
#             rabbit.get('exchange'),
#             config.get('QUEUES', queue_name),
#             rabbit.get('username'),
#             rabbit.get('password'),
#         )
#
#     def consume(self, callback):
#         self._channel.basic_consume(
#             queue=self._queue,
#             on_message_callback=callback)
#
#         def start_self():
#             self._channel.start_consuming()
#
#         consumer_thread = threading.Thread(target=start_self)
#         consumer_thread.daemon = True
#         consumer_thread.start()
#
#     def ack(self, tag):
#         self._channel.basic_ack(tag)
