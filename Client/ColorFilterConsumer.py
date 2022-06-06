import logging
import traceback

from Logger.CustomLogFormatter import CustomLogFormatter
from ColorFilter.ColorFilter import process_request
from Client import RabbitMQQueryListener
from Message import RabbitMQResponse

logger = logging.getLogger("ColorFilterConsumer")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomLogFormatter())
logger.addHandler(ch)

SERVICE_NAME = 'color_service'
QUEUE_CONFIG_NAME = 'colors'


if __name__ == '__main__':
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
