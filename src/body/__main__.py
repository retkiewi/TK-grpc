import grpc
import concurrent.futures
import core_body_pb2
import core_body_pb2_grpc

from body.face_detection import face_detection

server_port = '[::]:50052'

class Body(core_body_pb2_grpc.Body):
    def detect_face(self, target, *args, **kwargs):
        result = face_detection(target.path)
        return core_body_pb2.FaceResponse(return_value=result)


def main():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    core_body_pb2_grpc.add_BodyServicer_to_server(Body(), server)
    server.add_insecure_port(server_port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
