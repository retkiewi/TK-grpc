from core_size_pb2_grpc import SizeStub
from core_animal_pb2_grpc import AnimalStub
from core_format_pb2_grpc import FormatStub
from core_style_pb2_grpc import StyleStub
from core_body_pb2_grpc import BodyStub
from core_color_pb2_grpc import ColorStub
from core_dogs_pb2_grpc import DogsStub
from core_similarities_pb2_grpc import SimilaritiesStub


class GRPCStubProvider:
    @staticmethod
    def GetStub(name: str):
        return lambda channel: {
            'size': SizeStub(channel),
            'format': FormatStub(channel),
            'body': BodyStub(channel),
            'animal': AnimalStub(channel),
            'style': StyleStub(channel),
            'colors': ColorStub(channel),
            'dogs_breeds': DogsStub(channel),
            'similarity': SimilaritiesStub(channel)
        }[name]