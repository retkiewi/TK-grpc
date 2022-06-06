import grpc

from configparser import ConfigParser
from Connection.GRPCStubProvider import GRPCStubProvider


class GRPCConnection:
    @staticmethod
    def from_config(topic):
        config = ConfigParser()
        config.read('config.ini')

        return GRPCConnection(
            topic,
            config['GRPC'].get(topic),
        )

    def __init__(self, topic, address: str):
        self._channel = grpc.insecure_channel(address)
        self._stub = GRPCStubProvider.GetStub(topic)(self._channel)

    def get_result(self, request):
        return self._stub.get_result(request)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self._channel.close()
