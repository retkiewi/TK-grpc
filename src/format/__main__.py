import os
import grpc
import concurrent.futures
import core_format_pb2
import core_format_pb2_grpc

server_addr = '[::]:50051'

class Format(core_format_pb2_grpc.Format):
    def check_format(self, target, *args, **kwargs):
        result = check_for_formats(target.path, target.formats)
        return core_format_pb2.Response(return_value=result)


def main():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    core_format_pb2_grpc.add_FormatServicer_to_server(Format(), server)
    server.add_insecure_port(server_addr)
    server.start()
    server.wait_for_termination()


def check_for_formats(file_path: str, desired_formats: list[str]) -> bool:
    _, ext = os.path.splitext(file_path)
    return ext in desired_formats


if __name__ == '__main__':
    main()

