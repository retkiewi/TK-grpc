import logging
import traceback
import sys
from Client import GRPCQueryListener
from core_dogs_pb2_grpc import Dogs, add_DogsServicer_to_server as add_Dogs
from core_dogs_pb2 import DogsResponse
from Logger.CustomLogFormatter import CustomLogFormatter
from DogsFilter.DogsBreedFilter import process_request, process_single
from Client import RabbitMQQueryListener
from Message import RabbitMQResponse

logger = logging.getLogger("DogFilterConsumer")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomLogFormatter())
logger.addHandler(ch)

SERVICE_NAME = "dog_service"
QUEUE_CONFIG_NAME = 'dogs_breeds'


class DogsGRPC(Dogs):
    def get_result(self, target, *args, **kwargs):
        logger.info(f'recieved request for path {target.path}')
        res = process_single(target)
        logger.info(f'{res}: {type(res)}')
        return DogsResponse(return_value=res)


def setup_rmq():
    logger.info("Starting SimilarityConsumer")
    consumer = RabbitMQQueryListener(QUEUE_CONFIG_NAME)
    logger.info("SimilarityConsumer started successfully")

    def callback(ch, method, properties, body):
        logger.info(" [x] Received %r" % body)
        try:
            result = process_request(body)
            resp = RabbitMQResponse(200, result, SERVICE_NAME)
        except Exception as e:
            logging.error(traceback.format_exc())
            resp = RabbitMQResponse(500, [], SERVICE_NAME)
        consumer.respond(resp)

    consumer.listen(callback)


def setup_grpc():
    consumer = GRPCQueryListener()
    consumer.listen(lambda server: add_Dogs(
        DogsGRPC(), server), QUEUE_CONFIG_NAME)


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] == 'rmq':
        setup_rmq()
    else:
        setup_grpc()
