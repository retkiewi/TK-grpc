import logging
import traceback
from WeatherFilter.WeatherFilter import process_single

from Logger.CustomLogFormatter import CustomLogFormatter

from Client import GRPCQueryListener
from core_weather_pb2_grpc import Weather, add_WeatherServicer_to_server as add_Weather
from core_weather_pb2 import WeatherResponse

logger = logging.getLogger("WeatherFilterConsumer")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomLogFormatter())
logger.addHandler(ch)

QUEUE_CONFIG_NAME = 'weather'


class WeatherGRPC(Weather):
    def get_result(self, target, *args, **kwargs):
        logger.info(f'recieved request for path {target.path}')
        res = process_single(target)
        logger.info(f'{res}: {type(res)}')
        return WeatherResponse(return_value=res)


def setup_grpc():
    consumer = GRPCQueryListener()
    consumer.listen(lambda server: add_Weather(
        WeatherGRPC(), server), QUEUE_CONFIG_NAME)


if __name__ == '__main__':
    setup_grpc()
