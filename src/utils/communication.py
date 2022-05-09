import grpc

import core_animal_pb2
import core_animal_pb2_grpc
import core_format_pb2_grpc
import core_format_pb2
import core_body_pb2_grpc
import core_body_pb2
import core_style_pb2_grpc
import core_style_pb2

addresses = {'format' : 'localhost:50051', 'body' : 'localhost:50052', 'animal' : 'localhost:50053', 'style' : 'localhost:50054'}


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


class AnimalClient(GrpcClient):
    def __init__(self, address: str):
        super().__init__(address)
        self._stub = core_animal_pb2_grpc.AnimalStub(self._channel)

    def ask_for_animals(self, file_path: str, desired_animals: list[str]):
        request = core_animal_pb2.AnimalRequest(path=file_path, animals=desired_animals)
        response = self._stub.detect_animals(request)
        return response.return_values


class StyleClient(GrpcClient):
    def __init__(self, address: str):
        super().__init__(address)
        self._stub = core_style_pb2_grpc.StyleStub(self._channel)

    def ask_for_styles(self, file_path: str, desired_styles: list[str]):
        request = core_style_pb2.StyleRequest(path=file_path, styles=desired_styles)
        response = self._stub.check_style(request)
        return response.return_value


# def send_request(filter, values, path):
#     if filter == 'format':
#         with FormatClient(addresses['format']) as fc:
#             return fc.ask_for_formats(path, values)
#     if filter == 'body':
#         with BodyClient(addresses['body']) as bc:
#             return bc.ask_for_face(path)
#     if filter == 'animal':
#         with AnimalClient(addresses['animal']) as ac:
#             return ac.ask_for_animals(path, values)

def send_request(filters, path):
    results = {}
    if 'format' in filters:
        with FormatClient(addresses['format']) as fc:
            results['format'] = fc.ask_for_formats(path, filters['format'])
    if 'body' in filters:
        with BodyClient(addresses['body']) as bc:
            results['body'] = bc.ask_for_face(path)
    if 'animal' in filters:
        with AnimalClient(addresses['animal']) as ac:
            results['animal'] = ac.ask_for_animals(path, filters['animal'])
    if 'style' in filters:
        with StyleClient(addresses['style']) as sc:
            results['style'] = sc.ask_for_styles(path, filters['style'])
    return results




if __name__ == '__main__':
    srv_addr = 'localhost:50051'
    with FormatClient(srv_addr) as fc:
        print(fc.ask_for_formats('bubu.jpg', ['.jpg']))
        print(fc.ask_for_formats('bubu.jpg', ['.jp2']))

    srv_addr = 'localhost:50052'
    with BodyClient(srv_addr) as bc:
        print(bc.ask_for_face('dibi.png'))

    srv_addr = 'localhost:50053'
    with AnimalClient(srv_addr) as ac:
        print(ac.ask_for_animals('animal\\elephant.jpg', ["elephant"]))

    srv_addr = 'localhost:50054'
    with StyleClient(srv_addr) as ac:
        print(sc.ask_for_styles('animal\\elephant.jpg', ["clipart"]))
