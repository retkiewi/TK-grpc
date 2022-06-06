import logging

from Logger.CustomLogFormatter import CustomLogFormatter
from Message.MessageAbstracts import *

from Utils.Utils import get_comparator
from core_size_pb2 import SizeRequest
from core_animal_pb2 import AnimalRequest
from core_format_pb2 import FormatRequest
from core_style_pb2 import StyleRequest
from core_body_pb2 import BodyRequest

logger = logging.getLogger("Query")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomLogFormatter())
logger.addHandler(ch)


class SizeQuery(RabbitMQMessage, GRPCMessage):
    def __init__(self, paths, params, executor):
        super().__init__(paths, params, executor)

    @staticmethod
    def topic():
        return 'size'

    def grpc(self):
        values_raw = self.params[self.params['unit']]
        values = values_raw if isinstance(values_raw, list) else [float(values_raw)]
        for (k,v) in self.params.items():
            print(f'{k}:{type(v)}')
        return lambda path: SizeRequest(
            path=path,
            unit=self.params['unit'],
            comparator=self.params['comparator'],
            values=values
        )

    def approved(self, result) -> bool:
        return result


class DogsQuery(RabbitMQMessage):
    def __init__(self, paths, params, executor):
        super().__init__(paths, params, executor)

    @staticmethod
    def topic():
        return 'dogs_breeds'


class SimilarityQuery(RabbitMQMessage):
    def __init__(self, paths, params, executor):
        super().__init__(paths, params, executor)

    @staticmethod
    def topic():
        return 'similarity'


class FacesQuery(RabbitMQMessage):
    def __init__(self, paths, params, executor):
        super().__init__(paths, params, executor)

    @staticmethod
    def topic():
        return 'faces_smiles'


class ColorQuery(RabbitMQMessage):
    def __init__(self, paths, params, executor):
        super().__init__(paths, params, executor)

    @staticmethod
    def topic():
        return 'colors'


class FormatQuery(GRPCMessage):
    def __init__(self, paths, params, executor):
        super().__init__(paths, params, executor)

    @staticmethod
    def topic():
        return 'format'

    def grpc(self):
        return lambda path: FormatRequest(path=path, formats=self.params['formats'])

    def approved(self, result) -> bool:
        return result


class BodyQuery(GRPCMessage):
    def __init__(self, paths, params, executor):
        super().__init__(paths, params, executor)

    @staticmethod
    def topic():
        return 'body'

    def grpc(self):
        return lambda path: BodyRequest(path=path, types=self.params['types'])

    def approved(self, result) -> bool:
        comparator = get_comparator(self.params['comparator'])
        threshold = self.params('threshold')
        return any(map(lambda val: comparator(val, threshold), result))

class AnimalQuery(GRPCMessage):
    def __init__(self, paths, params, executor):
        super().__init__(paths, params, executor)

    @staticmethod
    def topic():
        return 'animal'

    def grpc(self):
        return lambda path: AnimalRequest(path=path, animals=self.params['animals'])

    def approved(self, result) -> bool:
        comparator = get_comparator(self.params['comparator'])
        threshold = self.params('threshold')
        return any(map(lambda val: comparator(val, threshold), result))


class StyleQuery(GRPCMessage):
    def __init__(self, paths, params, executor):
        super().__init__(paths, params, executor)

    @staticmethod
    def topic():
        return 'style'

    def grpc(self):
        return lambda path: StyleRequest(path=path, styles=self.params['styles'])

    def approved(self, result) -> bool:
        return result
