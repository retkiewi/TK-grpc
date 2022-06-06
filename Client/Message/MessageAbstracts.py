import json
from typing import Sequence
from abc import ABC, abstractmethod

from Message.Executor import Executor


class Message(ABC):
    __executor: Executor

    def __init__(self, paths: Sequence[str], params, executor: int):
        params = {k: v for k, v in params.items() if v is not None and v != ""}
        self.path_number = len(paths)
        self.paths = paths
        self.param_number = len(params)
        self.params = params
        self.executor = executor

    @staticmethod
    @abstractmethod
    def topic():
        ...


class JSONSupport(ABC):
    def json(self):
        return json.dumps(self.__dict__)


class GRPCSupport(ABC):
    @abstractmethod
    def grpc(self):
        """
        :return: A query dependent grpc Request instance
        """
        ...

    @abstractmethod
    def approved(self, result) -> bool:
        """
        Checks if result is compliant with query-dependent pass condition
        eg. When grpc returns similarity % checks if it's higher than threshold
        :param result: result of grpc call
        :return: check result
        """
        ...


class RabbitMQMessage(Message, JSONSupport, ABC):
    ...


class GRPCMessage(Message, GRPCSupport, ABC):
    ...


class HTTPMessage(Message, JSONSupport, ABC):
    ...
