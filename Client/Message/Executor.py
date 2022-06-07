import json
from enum import Enum


class Executor(int, Enum):
    RabbitMQ = 1,
    GRPC = 2,
    HTTP = 3
