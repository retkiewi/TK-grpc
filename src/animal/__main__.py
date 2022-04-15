import grpc
import concurrent.futures
import core_animal_pb2
import core_animal_pb2_grpc

from animal.animal_detection import detect_animals

server_port = '[::]:50052'

class Animal(core_animal_pb2_grpc.Animal):
    def detect_animals(self, target, *args, **kwargs):
        result = detect_animals(target.path)
        results = [result[animal] or 0 for animal in target.animals]
        return core_animal_pb2.AnimalResponse(return_values=results)


def main():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    core_animal_pb2_grpc.add_AnimalServicer_to_server(Animal(), server)
    server.add_insecure_port(server_port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
