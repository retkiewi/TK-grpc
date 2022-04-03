import grpc
import core_format_pb2_grpc
import core_format_pb2
import core_body_pb2_grpc
import core_body_pb2


class GrpcClient:
    def __init__(self, address: str):
        self._channel = grpc.insecure_channel(address)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self._channel.close()


class FormatClient(GrpcClient):
    def __init__(self, address: str):
        super().__init__(address)
        self._stub = core_format_pb2_grpc.FormatStub(self._channel)

    def ask_for_formats(self, file_path: str, desired_formats: list[str]) -> bool:
        request = core_format_pb2.FormatRequest(path=file_path,
                                        formats=desired_formats)
        response = self._stub.check_format(request)
        return response.return_value


class BodyClient(GrpcClient):
    def __init__(self, address: str):
        super().__init__(address)
        self._stub = core_body_pb2_grpc.BodyStub(self._channel)

    def ask_for_face(self, file_path: str) -> int:
        request = core_body_pb2.FaceRequest(path=file_path)
        response = self._stub.detect_face(request)
        return response.return_value



# if __name__ == '__main__':
if True:
    srv_addr = 'localhost:50051'
    with FormatClient(srv_addr) as fc:
        print(fc.ask_for_formats('bubu.jpg', ['.jpg']))
        print(fc.ask_for_formats('bubu.jpg', ['.jp2']))
    
    srv_addr = 'localhost:50052'
    with BodyClient(srv_addr) as bc:
        print(bc.ask_for_face('dibi.png'))
