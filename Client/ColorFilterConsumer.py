import logging
import sys
import traceback

from Client import GRPCQueryListener
from Logger.CustomLogFormatter import CustomLogFormatter
from ColorFilter.ColorFilter import process_request
from Client import RabbitMQQueryListener
from Message import RabbitMQResponse

from core_color_pb2_grpc import Color, add_ColorServicer_to_server as add_Color
from core_color_pb2 import ColorResponse

logger = logging.getLogger("ColorFilterConsumer")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomLogFormatter())
logger.addHandler(ch)

SERVICE_NAME = 'color_service'
QUEUE_CONFIG_NAME = 'colors'

class ColorGRPC(Color):
    def get_result(self, target, *args, **kwargs):
        logger.info(f'recieved request for path {target.path}')
        return ColorResponse(return_value=process_single(target))

def setup_rmq():
    logger.info("Starting ColorFilterConsumer")
    consumer = RabbitMQQueryListener(QUEUE_CONFIG_NAME)
    logger.info("ColorFilterConsumer started successfully")

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
    consumer.listen(lambda server: add_Color(ColorGRPC(), server), QUEUE_CONFIG_NAME)

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] == 'rmq':
        setup_rmq()
    else:
        setup_grpc()
