import grpc
import concurrent.futures

import core_style_pb2
import core_style_pb2_grpc
from style.style_detector import StyleDetector

server_port = '[::]:50054'

class Style(core_style_pb2_grpc.Style):
    def get_result(self, target, *args, **kwargs):
        style_detector = StyleDetector()
        result = style_detector.detect_style(target.path).value in target.styles
        return core_style_pb2.StyleResponse(return_value=result)


def main():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    core_style_pb2_grpc.add_StyleServicer_to_server(Style(), server)
    server.add_insecure_port(server_port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
