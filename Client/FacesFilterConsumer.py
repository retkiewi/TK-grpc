import logging
import traceback
import sys

from Client import GRPCQueryListener
from core_faces_pb2_grpc import Faces, add_FacesServicer_to_server as add_Face
from core_faces_pb2 import FacesResponse

from Logger.CustomLogFormatter import CustomLogFormatter
from FacesFilter.FacesFilter import process_request, process_single
from Client import RabbitMQQueryListener
from Message import RabbitMQResponse

logger = logging.getLogger("FacesFilterConsumer")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomLogFormatter())
logger.addHandler(ch)

SERVICE_NAME = "faces_service"
QUEUE_CONFIG_NAME = 'faces_smiles'

class FacesGRPC(Faces):
    def get_result(self, target, *args, **kwargs):
        logger.info(f'recieved request for path {target.path}')
        return FacesResponse(return_value=process_single(target))


def setup_rmq():
    logger.info("Starting FacesConsumer")
    consumer = RabbitMQQueryListener(QUEUE_CONFIG_NAME)
    logger.info("FacesConsumer started successfully")


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
    consumer.listen(lambda server: add_Face(FacesGRPC(), server), QUEUE_CONFIG_NAME)


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] == 'rmq':
        setup_rmq()
    else:
        setup_grpc()