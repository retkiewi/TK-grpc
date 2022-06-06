import logging

from Logger.CustomLogFormatter import CustomLogFormatter
from core_format_pb2_grpc import Format, add_FormatServicer_to_server as add_Format
from core_format_pb2 import FormatResponse
from format.format_checker import check_for_formats
from Client import GRPCQueryListener

logger = logging.getLogger("FormatService")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomLogFormatter())
logger.addHandler(ch)

QUEUE_CONFIG_NAME = 'format'

class FormatGRPC(Format):
    def get_result(self, target, *args, **kwargs):
        logger.info(f'recieved request for path {target.path}')
        result = check_for_formats(target.path, target.formats)
        return FormatResponse(return_value=result)


def main():
    consumer = GRPCQueryListener()
    consumer.listen(lambda server: add_Format(FormatGRPC(), server), QUEUE_CONFIG_NAME)


if __name__ == '__main__':
    main()

