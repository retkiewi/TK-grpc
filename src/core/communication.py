import grpc
import core_format_pb2_grpc
import core_format_pb2


class FormatClient:
    def __init__(self, address:str):
        self._channel = grpc.insecure_channel(address)
        self._stub = core_format_pb2_grpc.FormatStub(self._channel)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self._channel.close()

    def ask_for_formats(self, file_path: str, desired_formats: list[str]) -> bool:
        request = core_format_pb2.Request(path=file_path, formats=desired_formats)
        response = self._stub.check_format(request)
        return response.return_value


if __name__ == '__main__':
    client_addr = 'localhost:50051'
    with FormatClient(client_addr) as fc:
        print(fc.ask_for_formats('bubu.jpg', ['.jpg']))
        print(fc.ask_for_formats('bubu.jpg', ['.jp2']))
