import grpc
import concurrent.futures
import core_format_pb2
import core_format_pb2_grpc

from format.check_for_formats import check_for_formats

server_port = '[::]:50051'

class Format(core_format_pb2_grpc.Format):
    def check_format(self, target, *args, **kwargs):
        result = check_for_formats(target.path, target.formats)
        return core_format_pb2.FormatResponse(return_value=result)


def main():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    core_format_pb2_grpc.add_FormatServicer_to_server(Format(), server)
    server.add_insecure_port(server_port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()

