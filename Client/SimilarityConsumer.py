import logging
import sys
import traceback

from core_similarities_pb2 import SimilaritiesResponse
from core_similarities_pb2_grpc import Similarities, add_SimilaritiesServicer_to_server as add_Similarity

from Client import GRPCQueryListener
from Client import RabbitMQQueryListener
from Logger.CustomLogFormatter import CustomLogFormatter
from Message import RabbitMQResponse
from Similarity.SimilarityFilter import process_request, process_single

logger = logging.getLogger("SimilarityConsumer")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomLogFormatter())
logger.addHandler(ch)

SERVICE_NAME = "similarity_service"
QUEUE_CONFIG_NAME = 'similarity'


class SimilarityGRPC(Similarities):
    def get_result(self, target, *args, **kwargs):
        logger.info(f'recieved request for path {target.path}')
        return SimilaritiesResponse(return_value=process_single(target, logger))


def setup_rmq():
    logger.info("Starting SimilarityFilterConsumer")
    consumer = RabbitMQQueryListener(QUEUE_CONFIG_NAME)
    logger.info("SimilarityFilterConsumer started successfully")

    def callback(ch, method, properties, body):
        logger.info(" [x] Received %r" % body)
        try:
            result = process_request(body, logger)
            resp = RabbitMQResponse(200, result, SERVICE_NAME)
        except Exception as e:
            logging.error(traceback.format_exc())
            resp = RabbitMQResponse(500, [], SERVICE_NAME)
        consumer.respond(resp)

    consumer.listen(callback)


def setup_grpc():
    consumer = GRPCQueryListener()
    consumer.listen(lambda server: add_Similarity(SimilarityGRPC(), server), QUEUE_CONFIG_NAME)


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] == 'rmq':
        setup_rmq()
    else:
        setup_grpc()
