from core_size_pb2_grpc import SizeStub
from core_animal_pb2_grpc import AnimalStub
from core_format_pb2_grpc import FormatStub
from core_style_pb2_grpc import StyleStub
from core_body_pb2_grpc import BodyStub


class GRPCStubProvider:
    @staticmethod
    def GetStub(name: str):
        return lambda channel: {
            'size': SizeStub(channel),
            'format': FormatStub(channel),
            'body': BodyStub(channel),
            'animal': AnimalStub(channel),
            'style': StyleStub(channel)
        }[name]