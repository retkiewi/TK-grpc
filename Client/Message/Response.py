from typing import Sequence

from Message.MessageAbstracts import RabbitMQMessage, HTTPMessage


class RabbitMQResponse(RabbitMQMessage):
    def __init__(self, result: int, paths: Sequence[str], sender: str):
        super().__init__(paths, {}, 1)
        self.result = result
        self.paths = paths
        self.total = len(paths)
        self.sender = sender

    @staticmethod
    def topic():
        return 'results'


class HTTPResponse(HTTPMessage):
    ...

