import logging

from Logger.CustomLogFormatter import CustomLogFormatter
from Message.MessageAbstracts import *

from Utils.Utils import get_comparator
from core_size_pb2 import SizeRequest
from core_animal_pb2 import AnimalRequest
from core_format_pb2 import FormatRequest
from core_style_pb2 import StyleRequest
from core_body_pb2 import BodyRequest
from core_color_pb2 import ColorRequest
from core_dogs_pb2 import DogsRequest
from core_similarities_pb2 import SimilaritiesRequest
from core_faces_pb2 import FacesRequest
from core_people_pb2 import PeopleRequest
from core_metadata_pb2 import MetadataRequest

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
        return lambda path: SizeRequest(
            path=path,
            unit=self.params['unit'],
            comparator=self.params['comparator'],
            values=values
        )

    def approved(self, result) -> bool:
        return result


class DogsQuery(RabbitMQMessage, GRPCMessage):
    def __init__(self, paths, params, executor):
        super().__init__(paths, params, executor)

    @staticmethod
    def topic():
        return 'dogs_breeds'

    def grpc(self):
        return lambda path: DogsRequest(
            path=path,
            breed=self.params['breed']
        )

    def approved(self, result) -> bool:
        return result


class SimilarityQuery(RabbitMQMessage, GRPCMessage):
    def __init__(self, paths, params, executor):
        super().__init__(paths, params, executor)

    @staticmethod
    def topic():
        return 'similarity'

    def grpc(self):
        return lambda path: SimilaritiesRequest(
            path=path,
            percent=float(self.params['percent']),
            desired_path=self.params['path']
        )

    def approved(self, result) -> bool:
        return result


class FacesQuery(RabbitMQMessage, GRPCMessage):
    def __init__(self, paths, params, executor):
        super().__init__(paths, params, executor)

    @staticmethod
    def topic():
        return 'faces_smiles'

    def grpc(self):
        faces = int(self.params['no faces']) if 'no faces' in self.params else None
        smiles = int(self.params['no smiles']) if 'no smiles' in self.params else None
        threshold = float(self.params['threshold']) if 'threshold' in self.params else None
        return lambda path: FacesRequest(
            path=path,
            type=self.params['type'],
            faces=faces,
            smiles=smiles,
            comparator=self.params['comparator'],
            threshold=threshold,
        )

    def approved(self, result) -> bool:
        return result


class ColorQuery(RabbitMQMessage, GRPCMessage):
    def __init__(self, paths, params, executor):
        super().__init__(paths, params, executor)

    @staticmethod
    def topic():
        return 'colors'

    def grpc(self):
        threshold = float(self.params['threshold']) if 'threshold' in self.params else None
        percent_threshold = float(self.params['% threshold']) if '% threshold' in self.params else None
        tolerance = float(self.params['pixel tolerance']) if 'pixel tolerance' in self.params else None
        return lambda path: ColorRequest(
            path=path,
            system=self.params['system'],
            color=self.params['color'],
            metric=self.params['metric'],
            comparator=self.params['comparator'],
            threshold=threshold,
            percent_threshold=percent_threshold,
            tolerance=tolerance,
        )

    def approved(self, result) -> bool:
        return result


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
        comparator = get_comparator('>', 0)
        min_weight = float(self.params['minimal weight'])
        return any(map(lambda val: comparator(val, min_weight), result))


class AnimalQuery(GRPCMessage):
    def __init__(self, paths, params, executor):
        super().__init__(paths, params, executor)

    @staticmethod
    def topic():
        return 'animal'

    def grpc(self):
        return lambda path: AnimalRequest(path=path, animals=self.params['animals'])

    def approved(self, result) -> bool:
        comparator = get_comparator('>', 0)
        min_weight = float(self.params['minimal weight'])
        return any(map(lambda val: comparator(val, min_weight), result))


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

class PeopleQuery(GRPCMessage):
    def __init__(self, paths, params, executor):
        super().__init__(paths, params, executor)

    @staticmethod
    def topic():
        return 'people'

    def grpc(self):
        has_people =  self.params['has people'] == "true"

        params = dict()
        if 'min people' in self.params:
            params['min_people'] = int(self.params['min people'])
        if 'max people' in self.params:
            params['max_people'] = int(self.params['max people'])

        return lambda path: PeopleRequest(
            path=path,
            has_people=has_people,
            **params
        )

    def approved(self, result) -> bool:
        return result

class MetadataQuery(GRPCMessage):
    def __init__(self, paths, params, executor):
        super().__init__(paths, params, executor)

    @staticmethod
    def topic():
        return 'metadata'

    def grpc(self):
        params = dict()

        if 'exposure time' in self.params:
            params['exposureTime'] = float(self.params['exposure time'])
        if 'f number' in self.params:
            params['fNumber'] = float(self.params['f number'])
        if 'focal length' in self.params:
            params['focalLength'] = float(self.params['focal length'])
        if 'flash' in self.params:
            params['flash'] = float(self.params['flash'])
        if 'min pixel width' in self.params:
            params['pixelXDimMin'] = int(self.params['min pixel width'])
        if 'max pixel width' in self.params:
            params['pixelXDimMax'] = int(self.params['max pixel width'])
        if 'min pixel height' in self.params:
            params['pixelYDimMin'] = int(self.params['min pixel height'])
        if 'max pixel height' in self.params:
            params['pixelYDimMax'] = int(self.params['max pixel height'])

        return lambda path: MetadataRequest(
            path=path,
            **params
        )

    def approved(self, result) -> bool:
        return result

