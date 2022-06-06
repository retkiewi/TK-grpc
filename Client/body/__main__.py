import grpc
import concurrent.futures
import core_body_pb2
import core_body_pb2_grpc

from body.face_detection import face_detection
from body.hand_detection import hand_detection


server_port = '[::]:50052'

class Body(core_body_pb2_grpc.Body):
    def get_result(self, target, *args, **kwargs):
        results = {}
        if 'face' in target.types:
            results['face'] = face_detection(target.path)
        if 'hands' in target.types:
            results['hands'] = hand_detection(target.path)
        results = [results[part] if part in results else 0 for part in target.types]
        print(results)
        return core_body_pb2.BodyResponse(return_value=results)


def main():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    core_body_pb2_grpc.add_BodyServicer_to_server(Body(), server)
    server.add_insecure_port(server_port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
