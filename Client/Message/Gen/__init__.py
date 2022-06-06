from .core_size_pb2 import SizeRequest, SizeResponse
from .core_body_pb2 import BodyRequest, BodyResponse
from .core_style_pb2 import StyleRequest, StyleResponse
from .core_animal_pb2 import AnimalRequest, AnimalResponse
from .core_format_pb2 import FormatRequest, FormatResponse

from .core_size_pb2_grpc import SizeStub, Size, add_SizeServicer_to_server as add_Size
from .core_body_pb2_grpc import BodyStub, Body
from .core_style_pb2_grpc import StyleStub, Style
from .core_animal_pb2_grpc import AnimalStub, Animal
from .core_format_pb2_grpc import FormatStub, Format
