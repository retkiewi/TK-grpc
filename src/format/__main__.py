import os
import grpc
import core_format_pb2
import core_format_pb2_grpc
import concurrent.futures


def main():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    core_format_pb2_grpc.add_FormatServicer_to_server(Format(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


class Format(core_format_pb2_grpc.Format):
    def check_format(self,
                     target,
                     options=(),
                     channel_credentials=None,
                     call_credentials=None,
                     insecure=False,
                     compression=None,
                     wait_for_ready=None,
                     timeout=None,
                     metadata=None):
        return core_format_pb2.Response(response=check_for_formats(target.path, target.formats))


def check_for_formats(file_path: str, desired_formats: list[str]) -> bool:
    _, ext = os.path.splitext(file_path)
    return ext in desired_formats


if __name__ == '__main__':
    main()
