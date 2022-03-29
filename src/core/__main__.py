import grpc
import core_format_pb2_grpc
import core_format_pb2


def main():
    # TODO Start all components

    channel = grpc.insecure_channel('localhost:50051')
    stub = core_format_pb2_grpc.FormatStub(channel)
    response = stub.check_format(core_format_pb2.Request(path='C:/Users/pteki/UM/UM2/head_pose_estimation/headPose.jpg', formats=['.jpg']))
    print("Greeter client received: " + str(response.response))
    response = stub.check_format(core_format_pb2.Request(path='you', formats=['.jpg']))
    print("Greeter client received: " + str(response.response))
    pass    


if __name__ == '__main__':
    main()

